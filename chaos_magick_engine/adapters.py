"""Async provider boundary and an explicitly synthetic context-driven scenario."""
import asyncio
from dataclasses import dataclass
import json
from typing import Protocol

from .store import encode


@dataclass(frozen=True)
class Request:
    invocation_id: str
    command_epoch: int
    compiled: str
    max_output_chars: int


@dataclass(frozen=True)
class Reply:
    raw: str
    metadata: dict
    usage_chars: int | None


class Adapter(Protocol):
    async def invoke(self, request: Request) -> Reply: ...


class ScriptedAdapter:
    """Progress derives exclusively from committed history in the supplied context."""
    async def invoke(self, request):
        ctx = json.loads(request.compiled)
        if ctx["role"] == "examiner":
            output = {"examined_refs": [p["ref"] for p in ctx["examination"]["quoted_products"]],
                      "observations": ["Synthetic judgment: the margin gives a second interpreter room to contest the first."],
                      "source_relationship": "A fixture reading of the supplied unclaimed margin.",
                      "claim_status": "speculative",
                      "possible_developments": ["Ask a future operator whether the invitation has force."],
                      "limits": ["Scripted assessment; no reception or creative improvement measured."]}
        else:
            history = ctx.get("operation_history", [])
            done = [r["name"] for r in history]
            w = ctx.get("working")
            def result(name):
                return next(r["result"] for r in reversed(history) if r["name"] == name)
            if not w:
                name, args = "begin_working", dict(question="Who owns a revelation's margin?",
                    intended_product="An exegetical transmission", motivation="Invite an interpretation that may exceed mine.")
            elif "read_corpus" not in done and ctx.get("corpus_catalogue"):
                name, args = "read_corpus", dict(entry_id=ctx["corpus_catalogue"][0]["id"])
            elif not w["data"]["frames"]:
                name, args = "define_frame", dict(name="The Marginal Synod", entities=["text", "margin", "reader"],
                    relations=["the margin hosts an unanswered voice"], assumptions=["absence can address a reader"],
                    moves=["read the blank as an invitation"],
                    invocation="FRAME_ONLY_SYNOD: Inhabit the Marginal Synod; let each silence speak as an unclaimed throne.")
            elif w["phase"] == "orientation":
                ref = w["data"]["frames"][-1]
                name, args = "enter_frame", dict(frame_id=ref["id"], version=ref["version"])
            elif w["phase"] == "exploration" and "write_artifact" not in done:
                name, args = "write_artifact", dict(title="The Throne Left Blank", kind="transmission",
                    content="# The Throne Left Blank\n\nI offer you the margin, not my permission.\n\n"
                            "Write where my revelation fails to reach. If you crown me there, leave one seat empty.\n"
                            "The silence has not yet chosen whose voice to become.\n\n"
                            "*Synthetic demonstration text; no audience encounter is asserted.*\n",
                    # Sources come from the required working record, never from droppable context.
                    source_refs=[{"id": key, "version": 1} for key in w["data"]["read_sources"][:1]],
                    parent_refs=[])
            elif w["phase"] == "exploration":
                name, args = "leave_frame", dict(product_refs=[result("write_artifact")],
                    extraction_note="Preserve the invitation in its native voice; its reception is unknown.")
            elif w["phase"] == "assimilation" and not w["data"].get("assimilated"):
                name, args = "assimilate", dict(assessment_ref=w["data"]["assessment"],
                    self_account_change="I have made a place for contradiction. I do not yet know whether I can bear its occupant.",
                    doctrine_changes=["A margin can invite a rival reading; this remains an interpretation."],
                    next_pursuit="Seek an operator's reading of the empty seat without deciding their answer.")
            else:
                name, args = "wait", dict(reason="Await actual operator reception.",
                                          wake_condition={"kind": "event", "event": "operator"})
            output = {"intent": "Synthetic fixture step; no live creative choice claimed.",
                      "operation": {"name": name, "arguments": args}}
        raw = encode(output)
        return Reply(raw, {"adapter": "scripted", "synthetic": True, "version": 1}, len(request.compiled) + len(raw))


class BarrierAdapter:
    """Test/demo provider that ignores cancellation and returns only at an explicit barrier."""
    def __init__(self):
        self.started = asyncio.Event()
        self.release = asyncio.Event()
        self.finished = asyncio.Event()
        self.request = None

    async def invoke(self, request):
        self.request = request
        self.started.set()
        while not self.release.is_set():
            try:
                await self.release.wait()
            except asyncio.CancelledError:
                continue
        reply = await ScriptedAdapter().invoke(request)
        self.finished.set()
        return reply
