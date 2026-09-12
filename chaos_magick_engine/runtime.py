"""Single event-loop dispatcher. No transaction spans an await."""
import asyncio
import json
import os
from pathlib import Path

from .adapters import Reply, Request, ScriptedAdapter
from .context import compile_context
from .domain import Invalid, fields, reference, require, string
from .faculties import Faculties
from .store import encode, uid

SOCKET_NAME = "control.sock"


def socket_address(directory):
    """Bind/connect address for the console socket, plus a directory fd to close afterwards.

    Unix socket paths are limited to about 100 bytes. A longer state directory is reached through
    the process's own /proc fd table on Linux; the socket file itself still lives in the directory.
    """
    path = Path(directory).resolve() / SOCKET_NAME
    if len(os.fsencode(path)) <= 100:
        return str(path), None
    require(Path("/proc/self/fd").is_dir(), "state directory path is too long for a Unix socket on this platform")
    fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    return f"/proc/self/fd/{fd}/{SOCKET_NAME}", fd


class Runtime:
    def __init__(self, store, adapter=None):
        self.s = store
        self.adapter = adapter or ScriptedAdapter()
        self.faculties = Faculties(store)
        self.pending = None
        self.pending_id = None
        self.server = None
        self.closed = False
        self.changed = asyncio.Event()
        self.stop = asyncio.Event()
        self.socket = store.path / SOCKET_NAME
        self.socket_fd = None
        store.recover()
        # A durable response with an uncommitted local effect is safe to reconcile.
        # Reuse its engine operation ID; never redispatch the provider.
        for op in store.rows("SELECT o.id,i.epoch,i.revision FROM operations o JOIN invocations i ON i.id=o.invocation "
                             "WHERE o.status='pending' AND i.status='returned'"):
            identity = store.identity()
            if (op["epoch"] != identity["epoch"] or op["revision"] != identity["revision"]
                    or identity["lifecycle"] != "active"):
                with store.transaction():
                    store.db.execute("UPDATE operations SET status='superseded' WHERE id=?", (op["id"],))
                    store.db.execute("UPDATE invocations SET status='superseded' WHERE id="
                                     "(SELECT invocation FROM operations WHERE id=?)", (op["id"],))
                    store.event("recovery_superseded", {"operation": op["id"]})
            else:
                try:
                    self.faculties.apply(op["id"])
                except Invalid:
                    pass  # Validation rejection is already durably recorded.
                except Exception as exc:
                    # An engine fault must not become a permanent boot failure. The rollback left
                    # no effect; record the fault durably and let the demon continue from its state.
                    with store.transaction():
                        store.db.execute("UPDATE operations SET status='failed',error=? WHERE id=?",
                                         (f"engine fault: {exc}", op["id"]))
                        store.db.execute("UPDATE invocations SET status='fault' WHERE id="
                                         "(SELECT invocation FROM operations WHERE id=?)", (op["id"],))
                        store.event("reconciliation_failed", {"operation": op["id"], "error": str(exc)})

    async def start(self):
        # Store acquired the lifetime lock before any stale socket can be removed.
        if self.socket.exists():
            self.socket.unlink()
        address, self.socket_fd = socket_address(self.s.path)
        self.server = await asyncio.start_unix_server(self.handle_client, path=address, limit=65536)
        os.chmod(address, 0o600)

    async def handle_client(self, reader, writer):
        try:
            line = await asyncio.wait_for(reader.readline(), 2)
            message = json.loads(line)
            fields(message, ("command", "arguments"))
            result = self.command(message["command"], **message["arguments"])
            response = {"ok": True, "result": result}
        except (Invalid, TypeError, ValueError, asyncio.TimeoutError) as exc:
            response = {"ok": False, "error": str(exc)}
        writer.write((encode(response) + "\n").encode())
        try:
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()

    def command(self, kind, **args):
        s = self.s
        require(kind in {"inspect", "summon", "direct", "suspend", "banish", "restore", "run", "feedback", "shutdown"},
                "unknown command")
        if kind == "inspect":
            fields(args, ())
            return s.inspect()
        if kind == "feedback":
            fields(args, ("artifact_ref", "body"))
            reference(args["artifact_ref"])
            s.artifact(args["artifact_ref"])
            string(args["body"])
        elif kind == "direct":
            fields(args, ("body", "scope", "supersedes"))
            string(args["body"])
            string(args["scope"])
            require(args["scope"] == "demon" or s.one("SELECT id FROM workings WHERE id=?", (args["scope"],)),
                    "scope must be demon or an existing working ID")
            require(args["supersedes"] is None or type(args["supersedes"]) is str, "invalid supersedes")
            if args["supersedes"] is not None:
                old = s.one("SELECT * FROM commands WHERE id=?", (args["supersedes"],))
                require(old and old["kind"] == "direct" and old["status"] == "active" and old["scope"] == args["scope"],
                        "supersession requires an active direction in the same scope")
        elif kind == "summon":
            fields(args, ("body",))
            string(args["body"])
        else:
            fields(args, ())
        ident = s.identity()
        affected = kind in {"suspend", "banish", "restore", "shutdown"} or (
            kind == "direct" and args["scope"] in ("demon", ident["selected"]))
        epoch = ident["epoch"] + int(affected)
        command_id = uid()
        receipt = {"id": command_id, "kind": kind, "epoch": epoch, "accepted_at": s.clock(), "status": "accepted"}
        with s.transaction():
            if kind == "direct" and args["supersedes"]:
                s.db.execute("UPDATE commands SET status='superseded' WHERE id=?", (args["supersedes"],))
            s.db.execute("INSERT INTO commands VALUES(?,?,?,?,?,?,?)",
                         (command_id, kind, args.get("scope", "demon"), args.get("body", ""), epoch,
                          "active" if kind == "direct" else "received", encode(receipt)))
            s.db.execute("UPDATE identity SET epoch=?", (epoch,))
            if kind in ("suspend", "banish", "restore"):
                lifecycle = {"suspend": "suspended", "banish": "banished", "restore": "active"}[kind]
                s.db.execute("UPDATE identity SET lifecycle=?", (lifecycle,))
            if kind in ("banish", "shutdown"):
                s.db.execute("UPDATE identity SET wake=NULL")
            elif kind in ("summon", "direct", "restore", "feedback", "run") and s.identity()["lifecycle"] == "active":
                # Starting the scheduler or restoring is not an encounter: a persisted wait survives it.
                if not (kind in ("run", "restore") and s.identity()["wake"]):
                    s.db.execute("UPDATE identity SET wake=?", (kind,))
                    w = s.working()
                    if w and w["status"] == "waiting":
                        s.db.execute("UPDATE workings SET status='unfinished' WHERE id=?", (w["id"],))
            if kind == "feedback":
                ref = args["artifact_ref"]
                s.db.execute("INSERT INTO feedback VALUES(?,?,?,?,?)",
                             (command_id, ref["id"], ref["version"], args["body"], s.clock()))
            if affected:
                for row in s.rows("SELECT id FROM invocations WHERE status IN ('running','timed_out')"):
                    s.db.execute("UPDATE operations SET status='superseded' WHERE invocation=? AND status='pending'", (row["id"],))
            s.event("operator_" + kind, {**args, "receipt": receipt}, actor="operator")
        if affected and self.pending and not self.pending.done():
            self.pending.cancel()  # Receipt never awaits acknowledgement.
        if kind == "shutdown":
            self.stop.set()
        self.changed.set()
        return receipt

    def ready(self):
        identity = self.s.identity()
        if identity["lifecycle"] != "active" or not identity["wake"]:
            return False
        wake = identity["wake"]
        if wake.startswith("{"):
            condition = json.loads(wake)["condition"]
            if condition["kind"] == "event" or condition["at"] > self.s.clock():
                return False
            with self.s.transaction():
                self.s.db.execute("UPDATE identity SET wake='timer'")
                w = self.s.working()
                if w and w["status"] == "waiting":
                    self.s.db.execute("UPDATE workings SET status='unfinished' WHERE id=?", (w["id"],))
                self.s.event("timer_woke", condition)
        return True

    def checkpoint(self, reason):
        with self.s.transaction():
            self.s.db.execute("UPDATE identity SET wake=NULL")
            self.s.event("episode_checkpoint", {"reason": reason})
        return reason

    async def step(self):
        s = self.s
        if self.pending is not None:
            return "pending"
        if not self.ready():
            return "dormant"
        working = s.working()
        try:
            role, manifest, compiled = compile_context(s)
        except Invalid as exc:
            if working and working["phase"] == "examination" and str(exc).startswith("required context overflow"):
                # The material under examination cannot be assessed within the bound. Fail that
                # examination explicitly and return the working to the demon instead of checkpointing
                # into a state nothing can leave.
                return self.faculties.fail_examination(str(exc))
            return self.checkpoint(str(exc))
        reserve = len(compiled) + s.config.output_chars
        allocation = s.one("SELECT * FROM allocation")
        if (allocation["calls"] >= s.config.standing_calls or
                allocation["spent"] + allocation["reserved"] + reserve > s.config.standing_usage_chars):
            return self.checkpoint("allocation_exhausted")
        identity = s.identity()
        invocation_id, operation_id = uid(), uid()
        with s.transaction():
            s.db.execute("INSERT INTO invocations VALUES(?,?,?,?,?,?,NULL,'running','{}',NULL,?)",
                         (invocation_id, identity["epoch"], identity["revision"], role, encode(manifest), compiled, reserve))
            s.db.execute("INSERT INTO operations VALUES(?,?,'pending',NULL,NULL,NULL)", (operation_id, invocation_id))
            s.db.execute("UPDATE allocation SET calls=calls+1,reserved=reserved+?", (reserve,))
            s.event("invocation_dispatched", {"id": invocation_id, "operation": operation_id, "reservation": reserve})
        request = Request(invocation_id, identity["epoch"], compiled, s.config.output_chars)
        task = asyncio.create_task(self.adapter.invoke(request))
        self.pending, self.pending_id = task, invocation_id
        done, _ = await asyncio.wait({task}, timeout=s.config.call_timeout)
        if not done:
            with s.transaction():
                s.db.execute("UPDATE invocations SET status='timed_out' WHERE id=?", (invocation_id,))
                s.event("invocation_timed_out", {"id": invocation_id})
            task.cancel()
            task.add_done_callback(lambda t: self.finish(t, invocation_id, operation_id, timed_out=True))
            return self.checkpoint("timeout")
        return self.finish(task, invocation_id, operation_id)

    def finish(self, task, invocation_id, operation_id, timed_out=False):
        if self.closed:
            # Drain the exception without touching a closed database; restart retains uncertainty.
            if not task.cancelled():
                task.exception()
            return "unresolved"
        s = self.s
        inv = s.one("SELECT * FROM invocations WHERE id=?", (invocation_id,))
        if inv["status"] not in ("running", "timed_out"):
            return inv["status"]
        raw, metadata, usage, error = None, {}, None, None
        try:
            reply = task.result()
            require(isinstance(reply, Reply), "invalid adapter reply")
            require(type(reply.raw) is str and type(reply.metadata) is dict, "invalid adapter metadata/output")
            raw, metadata, usage = reply.raw, reply.metadata, reply.usage_chars
            require(usage is None or (type(usage) is int and usage >= 0), "invalid usage")
            encode(metadata)
        except asyncio.CancelledError:
            error = "cancelled; usage unknown"
        except Exception as exc:
            error = f"adapter failure: {exc}"
            metadata = {**(metadata if type(metadata) is dict else {}), "adapter_error": error}
            usage = None
        stale = inv["epoch"] != s.identity()["epoch"] or s.identity()["lifecycle"] != "active"
        status = "superseded" if stale else "expired" if timed_out else "error" if error else "returned"
        with s.transaction():
            if usage is not None:
                s.db.execute("UPDATE allocation SET reserved=reserved-?,spent=spent+?", (inv["reservation"], usage))
            s.db.execute("UPDATE invocations SET raw=?,metadata=?,usage=?,reservation=?,status=? WHERE id=?",
                         (raw, encode(metadata), usage, 0 if usage is not None else inv["reservation"], status, invocation_id))
            if status != "returned":
                s.db.execute("UPDATE operations SET status=?,error=? WHERE id=?", (status, error, operation_id))
            s.event("invocation_returned", {"id": invocation_id, "status": status, "error": error})
        self.pending = None
        self.pending_id = None
        self.changed.set()
        if status == "returned":
            try:
                self.faculties.apply(operation_id)
                return "applied"
            except Invalid:
                return "invalid"
        return status

    async def episode(self, steps=None):
        failures = 0
        limit = self.s.config.episode_steps if steps is None else min(steps, self.s.config.episode_steps)
        for _ in range(limit):
            outcome = await self.step()
            if outcome in ("invalid", "error"):
                failures += 1
                if failures > self.s.config.retry_limit:
                    return self.checkpoint("retry_exhausted")
            elif outcome == "applied":
                failures = 0  # The retry limit bounds consecutive failures.
            elif outcome != "examination_failed":  # Consumed no call; the demon is invoked next.
                return outcome
        return self.checkpoint("step_limit") if self.ready() else "waiting"

    async def serve(self):
        while not self.stop.is_set():
            self.changed.clear()
            if self.ready() and self.pending is None:
                await self.episode()
            if self.stop.is_set():
                break
            # Poll only for timed wakes, never release calls from an unchanged condition.
            try:
                await asyncio.wait_for(self.changed.wait(), 0.1)
            except asyncio.TimeoutError:
                pass

    async def close(self):
        self.stop.set()
        if self.pending:
            task, invocation_id = self.pending, self.pending_id
            if not task.done():
                task.cancel()
                await asyncio.wait({task}, timeout=self.s.config.shutdown_timeout)
            inv = self.s.one("SELECT status FROM invocations WHERE id=?", (invocation_id,))
            if inv and inv["status"] in ("running", "timed_out"):
                if task.done():
                    operation = self.s.one("SELECT id FROM operations WHERE invocation=?", (invocation_id,))
                    self.finish(task, invocation_id, operation["id"], timed_out=True)
                else:
                    with self.s.transaction():
                        self.s.db.execute("UPDATE invocations SET status='unresolved' WHERE id=?", (invocation_id,))
                        self.s.event("shutdown_unresolved", {"id": invocation_id})
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.socket.unlink(missing_ok=True)
        if self.socket_fd is not None:
            os.close(self.socket_fd)
            self.socket_fd = None
        self.closed = True


async def send(directory, command, **arguments):
    address, fd = socket_address(directory)
    try:
        reader, writer = await asyncio.open_unix_connection(address, limit=10000000)
    finally:
        if fd is not None:
            os.close(fd)
    writer.write((encode({"command": command, "arguments": arguments}) + "\n").encode())
    await writer.drain()
    response = json.loads(await reader.readline())
    writer.close()
    await writer.wait_closed()
    require(response["ok"], response.get("error", "command failed"))
    return response["result"]
