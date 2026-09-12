"""Local Unix console. Run directly from a checkout with Python 3.12+."""
import argparse
import asyncio
import json
from pathlib import Path
import signal
import sys

from .domain import Config, Invalid
from .runtime import Runtime, send
from .store import Store, encode

ROOT = Path(__file__).resolve().parent.parent


def initialize(directory, config_path):
    config = Config.from_dict(json.loads(Path(config_path).read_text()))
    source = (ROOT / "design/004-founding-demon.md").read_text()
    section = source.split("## Compact invocation seed\n", 1)[1].split("\n## ", 1)[0]
    seed = "\n".join(line[2:] if line.startswith("> ") else "" for line in section.splitlines() if line.startswith(">"))
    return Store(directory, initialize=True, config=config, seed=seed)


def export(s, directory, artifact_id=None):
    output = Path(directory)
    output.mkdir(parents=True, exist_ok=True)
    rows = s.rows("SELECT a.*,v.version,v.content FROM artifacts a JOIN versions v ON v.artifact_id=a.id "
                  "WHERE (? IS NULL OR a.id=?) ORDER BY a.rowid,v.version", (artifact_id, artifact_id))
    if artifact_id and not rows:
        raise Invalid("artifact unavailable")
    paths = []
    for row in rows:
        path = output / f"{row['id']}-v{row['version']}.md"
        path.write_text(f"<!-- Derived export: {row['id']} version {row['version']}; kind {row['kind']} -->\n\n{row['content']}\n")
        paths.append(str(path))
    return paths


def adapter_for(args):
    if getattr(args, "adapter", "scripted") != "claude":
        return None
    from .live import ClaudeAdapter
    return ClaudeAdapter(model=args.model, effort=args.effort, fallbacks=not args.no_fallbacks,
                         timeout=args.timeout, key_file=args.key_file)


async def live_check(args):
    """One small provider call through the same adapter, so the request shape is verified cheaply."""
    from .adapters import Request
    adapter = adapter_for(args)
    request = Request("live-check", 0, encode({"role": "demon", "instructions": "Reply with the JSON object "
                                               "{\"ok\": true, \"model\": \"<your model name>\"}.",
                                               "response_contract": {"envelope": {"ok": "boolean", "model": "string"}}}), 200)
    reply = await adapter.invoke(request)
    return {"raw": reply.raw, "metadata": reply.metadata, "usage_chars": reply.usage_chars}


async def run_async(s, args):
    runtime = Runtime(s, adapter_for(args))
    await runtime.start()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, runtime.stop.set)
    runtime.command("run")
    worker = asyncio.create_task(runtime.episode(args.steps) if args.once else runtime.serve())
    stopper = asyncio.create_task(runtime.stop.wait())
    try:
        done, _ = await asyncio.wait({worker, stopper}, return_when=asyncio.FIRST_COMPLETED)
        if worker in done:
            return worker.result()
        worker.cancel()
        await asyncio.gather(worker, return_exceptions=True)
        return "shutdown"
    finally:
        stopper.cancel()
        await runtime.close()


def bounded_loop(coroutine):
    # asyncio.run waits indefinitely for cancellation-resistant providers on exit.
    # The host owns this loop and closes it after Runtime's finite shutdown grace.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine)
    finally:
        for task in asyncio.all_tasks(loop):
            task.cancel()
            # Pending work is durably unresolved; loop termination is intentional.
            task._log_destroy_pending = False
        loop.close()
        asyncio.set_event_loop(None)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", default=".runtime/heresiarch")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init")
    p.add_argument("--config", default=str(ROOT / "demo/config.json"))
    p = sub.add_parser("import-corpus")
    p.add_argument("file")
    p.add_argument("--source")
    for name in ("run", "live-check"):
        p = sub.add_parser(name)
        if name == "run":
            p.add_argument("--once", action="store_true")
            p.add_argument("--steps", type=int)
        p.add_argument("--adapter", choices=("scripted", "claude"), default="scripted" if name == "run" else "claude")
        p.add_argument("--model", default="claude-opus-5")
        p.add_argument("--effort", choices=("low", "medium", "high", "xhigh", "max"), default="high")
        p.add_argument("--no-fallbacks", action="store_true", help="return policy declines instead of re-running on a fallback model")
        p.add_argument("--timeout", type=float, default=600.0, help="provider request timeout in seconds")
        p.add_argument("--key-file", help="file holding the API key; otherwise the SDK's own credential lookup applies")
    for name in ("inspect", "suspend", "banish", "restore", "shutdown", "verify"):
        sub.add_parser(name)
    p = sub.add_parser("summon")
    p.add_argument("body")
    p = sub.add_parser("direct")
    p.add_argument("body")
    p.add_argument("--scope", default="demon")
    p.add_argument("--supersedes")
    p = sub.add_parser("feedback")
    p.add_argument("artifact_id")
    p.add_argument("version", type=int)
    p.add_argument("body")
    p = sub.add_parser("export")
    p.add_argument("--output", required=True)
    p.add_argument("--artifact-id")
    p = sub.add_parser("demo")
    p.add_argument("--state-dir", dest="demo_state", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            from .demo import demonstration
            print(encode(demonstration(args.demo_state)))
            return 0
        if args.command == "live-check":
            print(encode(bounded_loop(live_check(args))))
            return 0
        if args.command == "init":
            s = initialize(args.state_dir, args.config)
            result = {"identity_id": s.identity()["id"]}
            s.close()
        elif args.command in {"inspect", "summon", "direct", "suspend", "banish", "restore", "feedback", "shutdown"}:
            payload = {}
            if args.command in ("summon", "direct", "feedback"):
                payload["body"] = args.body
            if args.command == "direct":
                payload.update(scope=args.scope, supersedes=args.supersedes)
            if args.command == "feedback":
                payload["artifact_ref"] = {"id": args.artifact_id, "version": args.version}
            try:
                result = bounded_loop(send(args.state_dir, args.command, **payload))
            except (FileNotFoundError, ConnectionRefusedError):
                # Offline commands still own the same writer lock and transaction path.
                s = Store(args.state_dir)
                try:
                    result = s.inspect() if args.command == "inspect" else Runtime(s).command(args.command, **payload)
                finally:
                    s.close()
        else:
            if args.command == "run" and not args.once:
                try:
                    result = bounded_loop(send(args.state_dir, "run"))  # An active server keeps its own adapter.
                except (FileNotFoundError, ConnectionRefusedError):
                    pass
                else:
                    print(encode(result))
                    return 0
            s = Store(args.state_dir)
            try:
                if args.command == "import-corpus":
                    result = {"entry_id": s.import_corpus(args.source or args.file, Path(args.file).read_bytes().decode("utf-8"))}
                elif args.command == "run":
                    if args.steps is not None and args.steps <= 0:
                        raise Invalid("steps must be positive")
                    result = bounded_loop(run_async(s, args))
                elif args.command == "verify":
                    result = {"issues": s.verify()}
                    if result["issues"]:
                        print(encode(result))
                        return 1
                else:
                    result = {"exports": export(s, args.output, args.artifact_id)}
            finally:
                s.close()
        print(encode(result))
        return 0
    except (Invalid, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
