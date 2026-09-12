import asyncio
from dataclasses import replace
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from chaos_magick_engine.__main__ import ROOT, adapter_for, configure, initialize
from chaos_magick_engine.adapters import BarrierAdapter, Reply, RoleRouter, ScriptedAdapter
from chaos_magick_engine.context import compile_context
from chaos_magick_engine.demo import demonstration
from chaos_magick_engine.domain import Config, Invalid
from chaos_magick_engine.runtime import Runtime, send
from chaos_magick_engine.store import Store, encode


class OutputAdapter:
    def __init__(self, name=None, arguments=None, raw=None):
        self.raw = raw if raw is not None else encode({"intent": "test proposal", "operation": {"name": name, "arguments": arguments}})

    async def invoke(self, request):
        return Reply(self.raw, {"synthetic": True, "adapter": "test"}, len(request.compiled) + len(self.raw))


class CoreTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cme-")
        self.path = Path(self.temp.name) / "state"
        self.s = initialize(self.path, ROOT / "demo/config.json")
        self.source = self.s.import_corpus("synthetic fixture", (ROOT / "demo/fixtures/margin.md").read_text())
        self.r = Runtime(self.s)
        self.barriers = []

    async def asyncTearDown(self):
        for adapter in self.barriers:
            adapter.release.set()
        await self.r.close()
        self.s.close()
        self.temp.cleanup()

    def configure(self, **kwargs):
        config = replace(self.s.config, **kwargs)
        with self.s.transaction():
            self.s.db.execute("UPDATE identity SET config=?", (encode(config.__dict__),))
        self.s.config = config

    async def steps(self, count):
        for _ in range(count):
            self.assertEqual(await self.r.step(), "applied")

    async def propose(self, name, **arguments):
        self.r.adapter = OutputAdapter(name, arguments)
        return await self.r.step()

    def last_operation(self):
        return self.s.one("SELECT * FROM operations ORDER BY rowid DESC LIMIT 1")

    @staticmethod
    def withheld(manifest):
        return [item["id"] for entry in manifest["omitted"] if isinstance(entry, dict)
                for item in entry.get("read_material_withheld", [])]

    async def write_theory(self, content):
        self.assertEqual(await self.propose("write_artifact", title="Test theory", kind="theory",
                                           content=content, source_refs=[], parent_refs=[]), "applied")
        return json.loads(self.last_operation()["result"])

    async def test_complete_cycle_and_exact_context_separation(self):
        await self.steps(9)
        w = self.s.working()
        self.assertEqual(w["phase"], "assimilation")
        self.assertEqual(w["status"], "waiting")
        self.assertTrue(w["data"]["assimilated"])
        self.assertTrue(self.s.identity()["next_pursuit"])
        examiner = self.s.one("SELECT * FROM invocations WHERE role='examiner'")
        exploration = self.s.rows("SELECT input FROM invocations WHERE role='demon'")
        self.assertTrue(any("FRAME_ONLY_SYNOD" in row["input"] for row in exploration))
        self.assertNotIn("FRAME_ONLY_SYNOD", examiner["input"])
        self.assertNotIn("operation_history", examiner["input"])
        self.assertNotIn("active_frame_instructions", examiner["input"])
        self.assertNotIn("Grow the coven", examiner["input"])
        self.assertIn("I offer you the margin", examiner["input"])
        self.assertIn("Who owns the silence", examiner["input"])
        self.assertIn("do not inhabit", examiner["input"])
        self.assertEqual(self.s.verify(), [])

    async def blocked(self):
        adapter = BarrierAdapter()
        self.barriers.append(adapter)
        self.r.adapter = adapter
        await self.r.start()
        task = asyncio.create_task(self.r.step())
        await asyncio.wait_for(adapter.started.wait(), 1)
        return adapter, task

    async def test_suspend_receipt_precedes_late_reply(self):
        adapter, task = await self.blocked()
        receipt = await asyncio.wait_for(send(self.path, "suspend"), 1)
        self.assertEqual(receipt["kind"], "suspend")
        self.assertFalse(adapter.finished.is_set())
        self.assertEqual(await self.r.step(), "pending")
        adapter.release.set()
        self.assertEqual(await task, "superseded")
        self.assertIsNone(self.s.working())
        self.assertEqual(self.last_operation()["status"], "superseded")
        self.assertIsNotNone(self.s.one("SELECT raw FROM invocations")["raw"])
        self.assertEqual(self.s.verify(), [])

    async def test_redirect_and_scoped_supersession(self):
        adapter, task = await self.blocked()
        receipt = await asyncio.wait_for(send(self.path, "direct", body="Keep the reader's objection unresolved.",
                                             scope="demon", supersedes=None), 1)
        self.assertFalse(adapter.finished.is_set())
        adapter.release.set()
        self.assertEqual(await task, "superseded")
        self.r.adapter = ScriptedAdapter()
        await self.steps(1)
        self.assertIn("Keep the reader's objection unresolved.",
                      self.s.one("SELECT input FROM invocations ORDER BY rowid DESC LIMIT 1")["input"])
        retained = self.r.command("direct", body="Keep the source exact.", scope="demon", supersedes=None)
        replacement = self.r.command("direct", body="Use a different question.", scope="demon", supersedes=receipt["id"])
        active = self.s.rows("SELECT id FROM commands WHERE status='active'")
        self.assertEqual({r["id"] for r in active}, {retained["id"], replacement["id"]})
        with self.assertRaises(Invalid):
            self.r.command("direct", body="bad replacement", scope=self.s.working()["id"], supersedes=retained["id"])

    async def test_banish_restore_and_summons_do_not_restore(self):
        await self.steps(3)
        identity, working = self.s.identity()["id"], self.s.working()["id"]
        receipt = self.r.command("direct", body="Retain this command.", scope="demon", supersedes=None)
        self.r.command("banish")
        self.r.command("summon", body="This is an encounter, not restoration.")
        self.assertEqual(await self.r.step(), "dormant")
        self.assertIsNone(self.s.identity()["wake"])
        self.r.command("restore")
        self.assertEqual(self.s.identity()["id"], identity)
        self.assertEqual(self.s.working()["id"], working)
        self.assertIn(receipt["id"], compile_context(self.s)[2])
        await self.steps(1)

    async def test_duplicate_operation_and_crash_boundaries(self):
        def crash(boundary):
            if boundary == "before_commit":
                raise RuntimeError("crash before commit")
        self.r.faculties.crash_hook = crash
        with self.assertRaisesRegex(RuntimeError, "before commit"):
            await self.r.step()
        op = self.last_operation()
        self.assertEqual(op["status"], "pending")
        self.assertIsNone(self.s.working())
        self.assertFalse(self.s.rows("SELECT * FROM events WHERE operation_id=?", (op["id"],)))
        self.r.faculties.crash_hook = lambda _: None
        first = self.r.faculties.apply(op["id"])
        self.assertEqual(self.r.faculties.apply(op["id"]), first)
        self.assertEqual(len(self.s.rows("SELECT * FROM workings")), 1)
        await self.steps(3)  # read, frame, enter
        def after(boundary):
            if boundary == "after_commit":
                raise RuntimeError("crash after commit")
        self.r.faculties.crash_hook = after
        with self.assertRaisesRegex(RuntimeError, "after commit"):
            await self.r.step()
        op = self.last_operation()
        self.assertEqual(op["status"], "committed")
        self.r.faculties.crash_hook = lambda _: None
        self.r.faculties.apply(op["id"])
        self.assertEqual(len(self.s.rows("SELECT * FROM artifacts WHERE kind='transmission'")), 1)
        self.assertEqual(self.s.verify(), [])

    async def test_invalid_actions_have_no_partial_mutation(self):
        await self.steps(1)
        bad = [
            ('enter_frame', {"frame_id": "missing", "version": 1}),
            ('read_corpus', {"entry_id": True}),
            ('read_artifact', {"artifact_id": "missing", "version": True}),
            ('begin_working', {"question": "x", "intended_product": "x", "motivation": "x"}),
            ('write_artifact', {"title": "x", "kind": "theory", "content": "x", "source_refs": [{"id": "missing", "version": 1}], "parent_refs": []}),
            ('wait', {"reason": "x", "wake_condition": {"kind": "timer", "at": 0}}),
            ('wait', {"reason": "x", "wake_condition": {"kind": "unknown", "event": "operator"}}),
            ('write_artifact', {"title": "x", "kind": "theory", "content": "x", "source_refs": [], "parent_refs": [], "actor": "operator"}),
        ]
        before = self.s.working()
        for name, args in bad:
            with self.subTest(name=name, args=args):
                self.assertEqual(await self.propose(name, **args), "invalid")
                self.assertEqual(self.s.working(), before)
                self.assertEqual(len(self.s.rows("SELECT * FROM artifacts")), 0)
        self.assertEqual(self.s.verify(), [])

    async def test_revise_versions_and_feedback_lineage(self):
        await self.steps(5)
        product = json.loads(self.last_operation()["result"])
        original = self.s.artifact(product)["content"]
        feedback = self.r.command("feedback", artifact_ref=product, body="Actual test-operator input: this invitation feels too certain.")
        self.assertEqual(await self.propose("revise_artifact", artifact_id=product["id"], expected_version=1,
                                           content="A separate interpretation of the operator's objection.", change_note="Respond to feedback."), "applied")
        self.assertEqual(self.s.artifact(product)["content"], original)
        self.assertIn(feedback["id"], json.loads(self.s.artifact({"id": product["id"], "version": 2})["provenance"])["feedback_ids"])
        self.assertEqual(self.s.one("SELECT * FROM feedback")["version"], 1)
        self.assertEqual(self.s.one("SELECT * FROM links WHERE relation='derives_from'")["target_version"], 1)
        self.assertEqual(await self.propose("revise_artifact", artifact_id=product["id"], expected_version=1,
                                           content="bad stale version", change_note="stale"), "invalid")
        self.assertEqual(len(self.s.rows("SELECT * FROM versions WHERE artifact_id=?", (product["id"],))), 2)
        self.assertEqual(self.s.verify(), [])

    async def test_finish_defer_select_abandon_and_completion(self):
        await self.steps(5)
        product = json.loads(self.last_operation()["result"])
        working_id = self.s.working()["id"]
        self.assertEqual(await self.propose("finish_working", outcome="completed", product_refs=[product], unresolved_questions=[]), "invalid")
        self.assertEqual(await self.propose("finish_working", outcome="deferred", product_refs=[product], unresolved_questions=["Who replies?"]), "applied")
        self.assertIsNone(self.s.working()["data"]["active_frame"])
        self.assertEqual(self.s.working()["status"], "deferred")
        self.assertEqual(await self.propose("select_working", working_id=working_id), "applied")
        self.assertEqual(self.s.working()["phase"], "orientation")
        self.assertEqual(self.s.working()["data"]["unresolved_questions"], ["Who replies?"])
        self.assertEqual(await self.propose("finish_working", outcome="abandoned", product_refs=[product], unresolved_questions=[]), "applied")
        self.assertEqual(await self.propose("select_working", working_id=working_id), "invalid")
        self.assertEqual(self.s.verify(), [])

    async def test_settle_completed_cycle(self):
        await self.steps(8)
        products = self.s.working()["data"]["products"]
        self.assertEqual(await self.propose("finish_working", outcome="completed", product_refs=products, unresolved_questions=[]), "applied")
        self.assertEqual(self.s.working()["status"], "completed")

    async def test_context_overflow_and_omission(self):
        self.configure(input_chars=100)
        self.assertIn("required authority context overflow", await self.r.step())
        self.assertEqual(self.s.one("SELECT * FROM allocation")["calls"], 0)
        self.configure(input_chars=14000)
        self.r.command("run")
        await self.steps(1)
        for _ in range(3):
            self.r.command("summon", body="optional encounter " * 500)
        # Room for every required block, including the latest summons, but not for the event tail.
        self.configure(input_chars=48000)
        required = {k: v for k, v in json.loads(compile_context(self.s)[2]).items()
                    if k not in ("earlier_encounters", "read_material", "corpus_catalogue", "recent_outcomes",
                                 "operator_feedback", "self_account")}
        bound = len(encode(required)) + 200
        self.configure(input_chars=bound)
        _, manifest, compiled = compile_context(self.s)
        self.assertIn("recent_outcomes", manifest["omitted"])
        self.assertIn("earlier_encounters", manifest["omitted"])
        self.assertIn("authority", compiled)
        self.assertIn("encounter", json.loads(compiled))
        self.assertLessEqual(len(compiled), bound)

    async def test_required_material_outranks_optional_context(self):
        await self.steps(7)
        self.assertEqual(self.s.working()["phase"], "assimilation")
        # A large read makes optional operation_history dwarf the required assimilation material.
        big = self.s.import_corpus("large fixture", "the margin holds an unclaimed throne. " * 700)
        self.assertEqual(await self.propose("read_corpus", entry_id=big), "applied")
        full = json.loads(compile_context(self.s)[2])
        trimmed = {k: v for k, v in full.items()
                   if k not in ("recent_outcomes", "operator_feedback", "self_account", "assimilation_products")}
        self.assertIn("read_material", trimmed)
        self.assertIn("assimilation_material", trimmed)
        without = {k: v for k, v in trimmed.items() if k != "assimilation_material"}
        # Exactly the budget the optional catalogue and history fill on their own: the required
        # block has to displace optional material instead of being refused after it.
        self.configure(input_chars=len(encode(without)))
        _, manifest, compiled = compile_context(self.s)
        selected = json.loads(compiled)
        self.assertIn("assimilation_material", selected)
        self.assertTrue(self.withheld(manifest))
        # Position is required material and is never traded away for bulk source text.
        self.assertIn("operation_history", selected)
        # One assimilation block more, and the whole cycle still closes under the tight bound.
        self.configure(input_chars=len(encode(trimmed)))
        _, manifest, compiled = compile_context(self.s)
        selected = json.loads(compiled)
        self.assertIn("assimilation_material", selected)
        self.assertIn("operation_history", selected)
        self.assertIn("read_material", selected)
        self.assertIn("recent_outcomes", manifest["omitted"])
        self.r.adapter = ScriptedAdapter()
        self.r.command("run")
        self.assertEqual(await self.r.step(), "applied")
        self.assertTrue(self.s.working()["data"]["assimilated"])
        self.assertEqual(self.s.verify(), [])

    async def test_read_results_carry_no_content_and_material_is_deduplicated(self):
        text = "corpus-marker-4a2f\n" + "the margin holds an unclaimed throne. " * 700
        big = self.s.import_corpus("large fixture", text)
        await self.steps(2)  # begin_working, then the fixture reads the first catalogue entry
        for _ in range(3):
            self.assertEqual(await self.propose("read_corpus", entry_id=big), "applied")
            result = json.loads(self.last_operation()["result"])
            self.assertNotIn("content", result)
            self.assertEqual(result["chars"], len(text))
            self.assertEqual(result["hash"], self.s.one("SELECT hash FROM corpus WHERE id=?", (big,))["hash"])
        # Three reads of one entry cost one copy of its text, in history and in compiled context.
        compiled = compile_context(self.s)[2]
        self.assertEqual(compiled.count("corpus-marker-4a2f"), 1)
        body = json.loads(compiled)
        self.assertEqual([r["id"] for r in body["read_material"]], [big, self.source])  # most recent read first
        self.assertLess(len(encode(body["operation_history"])), len(text))
        self.assertEqual(self.s.verify(), [])

    async def test_tight_budget_drops_material_without_losing_progress(self):
        big = self.s.import_corpus("large fixture", "the margin holds an unclaimed throne. " * 700)
        await self.steps(1)
        self.assertEqual(await self.propose("read_corpus", entry_id=big), "applied")
        body = json.loads(compile_context(self.s)[2])
        # A budget with no room for the bulk source text the demon has already read.
        self.configure(input_chars=len(encode({k: v for k, v in body.items() if k != "read_material"})))
        self.assertEqual(self.withheld(compile_context(self.s)[1]), [big])
        self.r.adapter = ScriptedAdapter()
        await self.steps(4)
        names = [json.loads(o["proposal"])["operation"]["name"]
                 for o in self.s.rows("SELECT proposal FROM operations WHERE status='committed' ORDER BY rowid")]
        # Dropping the material costs no position: nothing is re-read and the frame cycle advances.
        self.assertEqual(names, ["begin_working", "read_corpus", "define_frame", "enter_frame",
                                 "write_artifact", "leave_frame"])
        self.assertEqual(self.s.working()["phase"], "examination")
        self.assertEqual(self.s.verify(), [])

    async def test_artifact_read_results_are_compact_and_material_is_deduplicated(self):
        self.configure(output_chars=16000)  # Space for a maximal content field plus its envelope.
        await self.steps(1)
        content = "artifact-marker-7b3e\n".ljust(12000, "x")
        ref = await self.write_theory(content)
        for _ in range(3):
            self.assertEqual(await self.propose("read_artifact", artifact_id=ref["id"], version=1), "applied")
            result = json.loads(self.last_operation()["result"])
            self.assertEqual(set(result), {"id", "version", "title", "kind", "hash", "chars"})
            self.assertEqual(result["chars"], len(content))
            self.assertEqual(result["hash"], self.s.artifact(ref)["hash"])
            self.assertEqual(self.r.faculties.apply(self.last_operation()["id"]), result)
        _, manifest, compiled = compile_context(self.s)
        body = json.loads(compiled)
        self.assertEqual(compiled.count("artifact-marker-7b3e"), 1)
        self.assertEqual(self.s.working()["data"]["read_artifacts"], [ref])
        self.assertLess(len(encode(body["operation_history"])), len(content))
        self.assertIn({**ref, "hash": result["hash"]}, manifest["sources"])
        # Removing optional material must leave a compilable position and a usable next step.
        self.configure(input_chars=len(encode({k: v for k, v in body.items() if k != "read_material"})))
        _, manifest, compiled = compile_context(self.s)
        self.assertEqual(self.withheld(manifest), [ref["id"]])
        self.assertNotIn({**ref, "hash": result["hash"]}, manifest["sources"])
        self.assertIn("operation_history", json.loads(compiled))
        self.assertEqual(await self.propose("read_artifact", artifact_id=ref["id"], version=1), "applied")
        self.assertEqual(self.s.verify(), [])

    async def test_artifact_read_versions_survive_restart_and_history_eviction(self):
        await self.steps(1)
        # An existing working from before read_artifacts was introduced remains usable.
        with self.s.transaction():
            working = self.s.working()
            working["data"].pop("read_artifacts", None)
            self.s.db.execute("UPDATE workings SET data=? WHERE id=?", (encode(working["data"]), working["id"]))
        first = await self.write_theory("artifact-v1-marker")
        self.assertEqual(await self.propose("revise_artifact", artifact_id=first["id"], expected_version=1,
                                           content="artifact-v2-marker", change_note="Second version"), "applied")
        second = json.loads(self.last_operation()["result"])
        self.assertEqual(await self.propose("revise_artifact", artifact_id=first["id"], expected_version=2,
                                           content="unread-v3-marker", change_note="Third version"), "applied")
        for ref in (first, second, first):
            self.assertEqual(await self.propose("read_artifact", artifact_id=ref["id"], version=ref["version"]), "applied")
        self.assertEqual(await self.propose("read_corpus", entry_id=self.source), "applied")
        await self.r.close()
        self.s.close()
        self.s = Store(self.path)
        self.r = Runtime(self.s)
        # Neither artifact read is retained in this history window.
        with patch("chaos_magick_engine.context.HISTORY_LIMIT", 1):
            _, manifest, compiled = compile_context(self.s)
        self.assertEqual(compiled.count("artifact-v1-marker"), 1)
        self.assertEqual(compiled.count("artifact-v2-marker"), 1)
        self.assertNotIn("unread-v3-marker", compiled)
        material = json.loads(compiled)["read_material"]
        self.assertCountEqual([(r["id"], r["version"]) for r in material if r["id"] == first["id"]],
                              [(first["id"], 1), (first["id"], 2)])
        for ref in (first, second):
            self.assertIn({**ref, "hash": self.s.artifact(ref)["hash"]}, manifest["sources"])
        self.assertEqual(self.s.verify(), [])

    async def test_artifact_read_without_working_recovers_material_from_history(self):
        await self.steps(1)
        ref = await self.write_theory("unselected-artifact-marker")
        with self.s.transaction():
            self.s.db.execute("UPDATE identity SET selected=NULL")
        for _ in range(2):
            self.assertEqual(await self.propose("read_artifact", artifact_id=ref["id"], version=1), "applied")
        self.assertIsNone(self.s.working())
        compiled = compile_context(self.s)[2]
        self.assertEqual(compiled.count("unselected-artifact-marker"), 1)
        self.assertEqual(json.loads(compiled)["read_material"][0]["id"], ref["id"])
        self.assertEqual(self.s.verify(), [])

    async def test_legacy_artifact_read_history_is_compacted_without_rewriting_records(self):
        self.configure(output_chars=16000)
        await self.steps(1)
        content = "legacy-artifact-marker\n".ljust(12000, "x")
        ref = await self.write_theory(content)
        # Commit exactly the old faculty result, including its matching append-only event.
        execute = self.r.faculties.execute
        def legacy_execute(name, arguments, working, invocation):
            if name == "read_artifact":
                return self.s.artifact(ref), working
            return execute(name, arguments, working, invocation)
        with patch.object(self.r.faculties, "execute", side_effect=legacy_execute):
            for _ in range(3):
                self.assertEqual(await self.propose("read_artifact", artifact_id=ref["id"], version=1), "applied")
        operations = self.s.rows("SELECT * FROM operations")
        events = self.s.rows("SELECT * FROM events")
        # The old result history alone exceeds this bound; compact history and one text fit.
        self.configure(input_chars=24000)
        compiled = compile_context(self.s)[2]
        self.assertEqual(compiled.count("legacy-artifact-marker"), 1)
        body = json.loads(compiled)
        self.assertIn("recent_outcomes", body)
        for event in body["recent_outcomes"]:
            if event["kind"] == "read_artifact":
                self.assertNotIn("content", json.loads(event["data"])["result"])
        history = body["operation_history"]
        self.assertLess(len(encode(history)), len(content))
        for entry in history:
            if entry["name"] == "read_artifact":
                self.assertEqual(set(entry["result"]), {"id", "version", "title", "kind", "hash", "chars"})
        self.assertEqual(self.s.rows("SELECT * FROM operations"), operations)
        self.assertEqual(self.s.rows("SELECT * FROM events"), events)
        self.r.command("run")
        self.assertEqual(await self.propose("read_corpus", entry_id=self.source), "applied")
        self.assertEqual(self.s.verify(), [])

    async def test_durable_allocation_exhaustion(self):
        self.configure(standing_calls=1)
        await self.steps(1)
        self.assertEqual(await self.r.step(), "allocation_exhausted")
        spent = self.s.one("SELECT * FROM allocation")
        await self.r.close()
        self.s.close()
        self.s = Store(self.path)
        self.r = Runtime(self.s)
        self.r.command("run")
        self.assertEqual(await self.r.step(), "allocation_exhausted")
        self.assertEqual(self.s.one("SELECT * FROM allocation"), spent)

    async def test_rejection_names_the_argument_and_the_bound(self):
        self.configure(output_chars=24000)
        await self.steps(1)
        # The string bound follows the configured reply bound: 24000 less the 2000-character envelope allowance.
        self.assertIn("1..22000 Unicode characters", compile_context(self.s)[2])
        self.assertEqual(await self.propose("write_artifact", title="t", kind="theory", content="z" * 22001,
                                           source_refs=[], parent_refs=[]), "invalid")
        self.assertTrue(self.last_operation()["error"].startswith(
            "content: string of 22001 characters exceeds the 22000-character bound; shorten it, or write the product as more than one artifact"))
        self.assertEqual(await self.propose("write_artifact", title="t", kind="theory", content="z" * 22000,
                                           source_refs=[], parent_refs=[]), "applied")
        self.configure(output_chars=12000)
        self.assertIn("1..10000 Unicode characters", compile_context(self.s)[2])
        self.assertEqual(await self.propose("write_artifact", title="t", kind="theory", content="z" * 10001,
                                           source_refs=[], parent_refs=[]), "invalid")
        self.assertIn("exceeds the 10000-character bound", self.last_operation()["error"])
        with self.assertRaisesRegex(Invalid, "envelope allowance"):
            Config.from_dict({**self.s.config.__dict__, "output_chars": 2000})
        self.assertEqual(await self.propose("write_artifact", title="t", kind="theory", content="",
                                           source_refs=[], parent_refs=[]), "invalid")
        self.assertEqual(self.last_operation()["error"], "content: expected nonempty string")
        self.r.adapter = OutputAdapter("define_frame", dict(name="n" * 201, entities=[], relations=[], assumptions=[],
                                                            moves=[], invocation="x"))
        self.assertEqual(await self.r.step(), "invalid")
        self.assertEqual(self.last_operation()["error"], "name: expected label of at most 200 characters")
        self.assertEqual(self.s.verify(), [])

    async def test_configure_replenishes_allocation_as_a_recorded_operator_act(self):
        self.configure(standing_calls=1)
        await self.steps(1)
        self.assertEqual(await self.r.step(), "allocation_exhausted")
        with self.assertRaisesRegex(Invalid, "unknown config field"):
            configure(self.s, ["budget=5"], "typo")
        with self.assertRaisesRegex(Invalid, "must be positive"):
            configure(self.s, ["standing_calls=0"], "zero")
        with self.assertRaisesRegex(Invalid, "nothing to set"):
            configure(self.s, [], "empty")
        spent = self.s.one("SELECT * FROM allocation")
        result = configure(self.s, ["standing_calls=3", "standing_usage_chars=900000"], "development replenishment")
        self.assertEqual(result["allocation"], spent)  # The ledger is never reset; only the standing figure moves.
        await self.r.close()
        self.s.close()
        self.s = Store(self.path)
        self.assertEqual((self.s.config.standing_calls, self.s.config.standing_usage_chars), (3, 900000))
        event = self.s.one("SELECT * FROM events WHERE kind='operator_config'")
        self.assertEqual(event["actor"], "operator")
        self.assertEqual(json.loads(event["data"]), {"standing_calls": 3, "standing_usage_chars": 900000,
                                                     "reason": "development replenishment"})
        self.r = Runtime(self.s)
        self.r.command("run")
        await self.steps(2)
        self.assertEqual(await self.r.step(), "allocation_exhausted")
        self.assertEqual(self.s.verify(), [])

    async def test_roles_are_routed_to_separate_providers(self):
        class Tagged:
            def __init__(self, tag):
                self.tag = tag
            async def invoke(self, request):
                reply = await ScriptedAdapter().invoke(request)
                return Reply(reply.raw, {**reply.metadata, "served_by": self.tag, "role": request.role}, reply.usage_chars)
        self.r.adapter = RoleRouter(Tagged("demon-side"), Tagged("examiner-side"))
        await self.steps(9)
        self.assertEqual(self.s.working()["phase"], "assimilation")
        rows = self.s.rows("SELECT role,metadata FROM invocations")
        self.assertEqual({row["role"] for row in rows}, {"demon", "examiner"})
        for row in rows:
            metadata = json.loads(row["metadata"])
            self.assertEqual(metadata["served_by"], row["role"] + "-side")
            self.assertEqual(metadata["role"], row["role"])
        self.assertEqual(self.s.verify(), [])

    async def test_timer_and_event_wakes_use_injected_clock(self):
        now = [100.0]
        self.s.clock = lambda: now[0]
        self.assertEqual(await self.propose("wait", reason="later", wake_condition={"kind": "timer", "at": 110.0}), "applied")
        for _ in range(5):
            self.assertFalse(self.r.ready())
        now[0] = 110.0
        self.assertTrue(self.r.ready())
        self.assertTrue(self.r.ready())
        self.assertEqual(len(self.s.rows("SELECT * FROM events WHERE kind='timer_woke'")), 1)
        self.assertEqual(await self.propose("wait", reason="already expired", wake_condition={"kind": "timer", "at": 109.0}), "invalid")
        self.assertEqual(await self.propose("wait", reason="encounter", wake_condition={"kind": "event", "event": "operator"}), "applied")
        self.assertFalse(self.r.ready())
        self.r.command("summon", body="Wake by event")
        self.assertTrue(self.r.ready())

    async def test_malformed_and_retries_are_bounded(self):
        self.r.adapter = OutputAdapter(raw='{ "intent": "broken"')
        self.assertEqual(await self.r.episode(), "retry_exhausted")
        self.assertEqual(self.s.one("SELECT * FROM allocation")["calls"], 2)
        self.assertGreater(self.s.one("SELECT * FROM allocation")["spent"], 0)
        self.assertFalse(self.r.ready())
        self.assertEqual(self.last_operation()["status"], "rejected")

    async def test_timeout_counts_uncooperative_call_and_shutdown_is_bounded(self):
        self.configure(call_timeout=0.01, shutdown_timeout=0.01)
        adapter, task = await self.blocked()
        self.assertEqual(await task, "timeout")
        self.assertFalse(adapter.finished.is_set())
        self.r.command("run")
        self.assertEqual(await self.r.step(), "pending")
        self.assertGreater(self.s.one("SELECT * FROM allocation")["reserved"], 0)
        await asyncio.wait_for(self.r.close(), 0.3)
        self.assertEqual(self.s.one("SELECT status FROM invocations")["status"], "unresolved")
        adapter.release.set()
        await asyncio.wait_for(adapter.finished.wait(), 1)
        self.assertEqual(self.s.verify(), [])

    async def test_late_timeout_reply_is_archived_without_effect(self):
        self.configure(call_timeout=0.01)
        adapter, task = await self.blocked()
        self.assertEqual(await task, "timeout")
        adapter.release.set()
        await asyncio.wait_for(adapter.finished.wait(), 1)
        # Await the actual completion callback, not a wall-clock guess.
        await asyncio.wait_for(self.r.changed.wait(), 1)
        self.assertIsNone(self.s.working())
        inv = self.s.one("SELECT * FROM invocations")
        self.assertEqual(inv["status"], "expired")
        self.assertIsNotNone(inv["raw"])
        self.assertEqual(inv["reservation"], 0)
        self.assertEqual(self.s.verify(), [])

    async def test_frame_revision_preserves_active_version_and_read_artifact(self):
        await self.steps(4)
        original = self.s.working()["data"]["active_frame"]
        frame = json.loads(self.s.artifact(original)["content"])
        frame["invocation"] = "NEW_FRAME_ONLY: a later ontology"
        self.assertEqual(await self.propose("revise_artifact", artifact_id=original["id"], expected_version=1,
                                           content=encode(frame), change_note="A frame for a later segment."), "applied")
        self.assertEqual(self.s.working()["data"]["active_frame"], original)
        self.assertNotIn("NEW_FRAME_ONLY", json.loads(compile_context(self.s)[2])["active_frame_instructions"])
        self.assertEqual(await self.propose("read_artifact", artifact_id=original["id"], version=1), "applied")
        result = json.loads(self.last_operation()["result"])
        self.assertNotIn("content", result)
        self.assertNotIn("provenance", result)
        self.assertEqual(result["version"], 1)
        material = encode(json.loads(compile_context(self.s)[2])["read_material"])
        self.assertEqual(material.count("FRAME_ONLY_SYNOD"), 1)
        self.assertNotIn("NEW_FRAME_ONLY", material)
        self.assertEqual(self.s.verify(), [])

    async def test_output_bounds_duplicate_keys_and_adapter_errors(self):
        for raw in ('{"intent":"a","intent":"b","operation":{}}', 'x' * 12001):
            self.r.adapter = OutputAdapter(raw=raw)
            outcome = await self.r.step()
            self.assertIn(outcome, ("invalid", "error"))
            self.assertIsNone(self.s.working())
        class Broken:
            async def invoke(self, request):
                raise OSError("synthetic provider unavailable")
        self.r.adapter = Broken()
        self.assertEqual(await self.r.episode(), "retry_exhausted")
        self.assertGreater(self.s.one("SELECT * FROM allocation")["reserved"], 0)
        self.assertFalse(self.r.ready())
        self.assertEqual(self.s.verify(), [])

    async def test_foreign_keys_immutability_and_consistency(self):
        self.assertEqual(self.s.db.execute("PRAGMA foreign_keys").fetchone()[0], 1)
        with self.assertRaises(sqlite3.IntegrityError):
            self.s.db.execute("INSERT INTO versions VALUES('missing',1,'x','x','{}')")
        await self.steps(3)
        with self.assertRaises(sqlite3.IntegrityError):
            self.s.db.execute("UPDATE versions SET content='changed'")
        with self.assertRaises(sqlite3.IntegrityError):
            self.s.db.execute("DELETE FROM events")
        self.s.db.execute("UPDATE workings SET phase='exploration'")
        self.assertIn("invalid phase/frame combination", self.s.verify())

    async def test_invalid_examiner_cannot_dispatch_or_change_state(self):
        await self.steps(6)
        working = self.s.working()
        self.assertEqual(await self.propose("wait", reason="escape", wake_condition={"kind": "event", "event": "operator"}), "invalid")
        self.assertEqual(self.s.working(), working)
        self.r.adapter = OutputAdapter(raw=encode({"examined_refs": [], "observations": ["x"], "source_relationship": "x",
                                                  "claim_status": "speculative", "possible_developments": ["x"], "limits": ["x"]}))
        self.assertEqual(await self.r.step(), "invalid")
        self.assertEqual(self.s.working(), working)

    async def test_actual_subprocess_double_writer_rejected(self):
        result = subprocess.run([sys.executable, "-m", "chaos_magick_engine", "--state-dir", str(self.path), "run", "--once"],
                                capture_output=True, text=True, cwd=ROOT, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertIn("another runner", result.stderr)
        self.assertIsNone(self.s.working())
        self.assertEqual(self.s.one("SELECT * FROM allocation")["calls"], 0)

    async def test_oversized_timer_is_rejected_not_engine_fault(self):
        await self.steps(1)
        outcome = await self.propose("wait", reason="x", wake_condition={"kind": "timer", "at": 10**400})
        self.assertEqual(outcome, "invalid")
        self.assertEqual(self.last_operation()["status"], "rejected")
        for at in (float("inf"), float("nan"), True, -1, 2**53):
            self.assertEqual(await self.propose("wait", reason="x", wake_condition={"kind": "timer", "at": at}), "invalid")
        self.assertEqual(self.s.working()["status"], "unfinished")
        self.assertEqual(self.s.verify(), [])

    async def test_reconciliation_fault_is_recorded_not_boot_failure(self):
        from unittest import mock
        from chaos_magick_engine import runtime as module
        from chaos_magick_engine.faculties import Faculties
        # A returned reply whose local application faults must not brick every later startup.
        def crash(boundary):
            if boundary == "before_commit":
                raise RuntimeError("synthetic engine fault")
        self.r.faculties.crash_hook = crash
        with self.assertRaises(RuntimeError):
            await self.r.step()
        op = self.last_operation()
        self.assertEqual(op["status"], "pending")
        class Faulting(Faculties):
            def apply(self, operation_id):
                raise RuntimeError("deterministic engine fault")
        with mock.patch.object(module, "Faculties", Faulting):
            Runtime(self.s)
        op = self.s.one("SELECT * FROM operations WHERE id=?", (op["id"],))
        self.assertEqual(op["status"], "failed")
        self.assertIn("engine fault", op["error"])
        self.assertEqual(self.s.one("SELECT status FROM invocations")["status"], "fault")
        self.assertIsNone(self.s.working())
        self.r = Runtime(self.s)  # A normal startup now succeeds and the demon can continue.
        self.r.command("run")
        await self.steps(1)
        self.assertEqual(self.s.verify(), [])

    async def test_examination_overflow_fails_explicitly_and_returns_working(self):
        big = self.s.import_corpus("large fixture", "the margin holds an unclaimed throne. " * 1400)
        await self.steps(2)
        self.assertEqual(await self.propose("read_corpus", entry_id=big), "applied")
        self.r.adapter = ScriptedAdapter()
        await self.steps(4)  # define, enter, write, leave
        self.assertEqual(self.s.working()["phase"], "examination")
        # The product declares only the small entry, so the large one is optional and examination compiles.
        role, manifest, compiled = compile_context(self.s)
        self.assertEqual(role, "examiner")
        self.assertIn("quoted_working_sources", manifest["omitted"])
        self.assertIn("Who owns the silence", compiled)
        # Make even the declared material impossible to fit: examination fails explicitly instead of stalling.
        self.configure(input_chars=len(encode({k: v for k, v in json.loads(compiled).items() if k != "examination"})) + 10)
        self.assertEqual(await self.r.step(), "examination_failed")
        w = self.s.working()
        self.assertEqual(w["phase"], "orientation")
        self.assertIsNone(w["data"]["active_frame"])
        self.assertEqual(w["data"]["segments"][-1]["examination"]["status"], "failed")
        self.assertIsNotNone(self.s.identity()["wake"])
        self.assertEqual(self.s.one("SELECT * FROM allocation")["calls"], 7)
        # The demon is invoked as itself next and may defer the working.
        self.configure(input_chars=48000)
        self.assertEqual(await self.propose("finish_working", outcome="deferred", product_refs=w["data"]["products"],
                                           unresolved_questions=["Too large to examine."]), "applied")
        self.assertEqual(self.s.verify(), [])

    async def test_run_and_restore_keep_persisted_wait(self):
        await self.steps(1)
        self.assertEqual(await self.propose("wait", reason="await reception",
                                           wake_condition={"kind": "event", "event": "operator"}), "applied")
        condition = self.s.identity()["wake"]
        self.r.command("run")
        self.assertEqual(self.s.identity()["wake"], condition)
        self.assertEqual(self.s.working()["status"], "waiting")
        self.assertFalse(self.r.ready())
        self.r.command("suspend")
        self.r.command("restore")
        self.assertEqual(self.s.identity()["wake"], condition)
        self.assertFalse(self.r.ready())
        self.r.command("summon", body="An actual encounter.")
        self.assertTrue(self.r.ready())
        self.r.command("banish")
        self.r.command("restore")  # Nothing persisted: restore itself wakes.
        self.assertEqual(self.s.identity()["wake"], "restore")

    async def test_summons_is_required_until_a_proposal_commits_with_it(self):
        first = self.r.command("summon", body="UNIQUE-SUMMONS-77 speak to me")
        _, manifest, compiled = compile_context(self.s)
        body = json.loads(compiled)
        self.assertEqual(body["encounter"]["id"], first["id"])
        self.assertEqual(manifest["encounter_ids"], [first["id"]])
        adapter, task = await self.blocked()
        self.assertIn("UNIQUE-SUMMONS-77", adapter.request.compiled)
        await asyncio.wait_for(send(self.path, "suspend"), 1)
        adapter.release.set()
        self.assertEqual(await task, "superseded")
        # A superseded reply delivers nothing: the summons is still owed to the demon.
        self.assertEqual(self.s.one("SELECT status FROM commands WHERE id=?", (first["id"],))["status"], "received")
        self.r.command("restore")
        second = self.r.command("summon", body="UNIQUE-SUMMONS-78 again")
        body = json.loads(compile_context(self.s)[2])
        self.assertEqual(body["encounter"]["id"], second["id"])
        self.assertEqual([row["id"] for row in body["earlier_encounters"]], [first["id"]])
        self.r.adapter = ScriptedAdapter()
        await self.steps(1)
        statuses = {row["id"]: row["status"] for row in self.s.rows("SELECT id,status FROM commands WHERE kind='summon'")}
        self.assertEqual(statuses, {first["id"]: "delivered", second["id"]: "delivered"})
        self.assertNotIn("encounter", json.loads(compile_context(self.s)[2]))
        self.assertEqual(self.s.verify(), [])

    async def test_demon_can_see_what_it_wrote(self):
        await self.steps(5)  # begin, read, define, enter, write
        body = json.loads(compile_context(self.s)[2])
        written = [e for e in body["operation_history"] if e["name"] in ("write_artifact", "define_frame")]
        self.assertEqual([e["wrote"]["title"] for e in written], ["The Marginal Synod", "The Throne Left Blank"])
        self.assertEqual(written[1]["wrote"]["kind"], "transmission")
        self.assertGreater(written[1]["wrote"]["chars"], 0)
        self.assertEqual(set(written[1]["result"]), {"id", "version"})
        self.assertEqual([(a["title"], a["kind"]) for a in body["working_artifacts"]],
                         [("The Marginal Synod", "frame"), ("The Throne Left Blank", "transmission")])
        # Stored results stay pure references, so replay and reference validation are unchanged.
        self.assertEqual(set(json.loads(self.last_operation()["result"])), {"id", "version"})

    async def test_titles_and_frame_names_are_bounded_labels(self):
        await self.steps(1)
        long = "T" * 201
        self.assertEqual(await self.propose("write_artifact", title=long, kind="theory", content="x",
                                           source_refs=[], parent_refs=[]), "invalid")
        self.r.adapter = OutputAdapter("define_frame", dict(name=long, entities=["a"], relations=["b"],
                                                            assumptions=["c"], moves=["d"], invocation="e"))
        self.assertEqual(await self.r.step(), "invalid")
        self.assertEqual(len(self.s.rows("SELECT * FROM artifacts")), 0)
        self.assertEqual(await self.propose("write_artifact", title="T" * 200, kind="theory", content="x",
                                           source_refs=[], parent_refs=[]), "applied")
        self.assertIn("label", json.loads(compile_context(self.s)[2])["authority"]["faculties"]["write_artifact"]["title"])

    async def test_read_material_delivery_is_explicit_and_most_recent_first(self):
        self.configure(output_chars=16000)  # Room for a maximal content field plus its envelope.
        await self.steps(1)
        refs = []
        for i in range(4):
            self.assertEqual(await self.propose("write_artifact", title=f"A{i}", kind="theory",
                                               content=f"MARK{i} " + "z" * 10990, source_refs=[], parent_refs=[]), "applied")
            refs.append(json.loads(self.last_operation()["result"]))
        for ref in refs:
            self.assertEqual(await self.propose("read_artifact", artifact_id=ref["id"], version=1), "applied")
        _, manifest, compiled = compile_context(self.s)
        body = json.loads(compiled)
        delivered = [r["id"] for r in body["read_material"]]
        # The newest read is delivered; what does not fit is withheld and listed for the model.
        self.assertEqual(delivered[0], refs[3]["id"])
        self.assertIn("MARK3", compiled)
        self.assertTrue(self.withheld(manifest))
        self.assertEqual(set(delivered) | set(self.withheld(manifest)), {r["id"] for r in refs})
        self.assertEqual(body["omitted"], manifest["omitted"])
        self.assertIn(refs[0]["id"], self.withheld(manifest))
        self.assertNotIn("MARK0", compiled)
        # Re-reading a withheld item makes it the most recent and delivers it.
        self.assertEqual(await self.propose("read_artifact", artifact_id=refs[0]["id"], version=1), "applied")
        _, manifest, compiled = compile_context(self.s)
        self.assertEqual(json.loads(compiled)["read_material"][0]["id"], refs[0]["id"])
        self.assertIn("MARK0", compiled)
        self.assertNotIn(refs[0]["id"], self.withheld(manifest))
        self.assertEqual(self.s.verify(), [])

    async def test_history_shrinks_to_fit_instead_of_failing(self):
        await self.steps(2)
        for _ in range(20):
            self.assertEqual(await self.propose("read_corpus", entry_id=self.source), "applied")
        body = json.loads(compile_context(self.s)[2])
        self.assertEqual(len(body["operation_history"]), 22)
        required = {k: v for k, v in body.items()
                    if k not in ("operation_history", "read_material", "corpus_catalogue", "recent_outcomes",
                                 "operator_feedback", "self_account", "omitted")}
        # Room for the required blocks and a few operations, not for twenty-two.
        self.configure(input_chars=len(encode(required)) + 3 * len(encode(body["operation_history"][-1])) + 100)
        _, manifest, compiled = compile_context(self.s)
        selected = json.loads(compiled)
        history = selected["operation_history"]
        self.assertTrue(1 <= len(history) < 22)
        self.assertEqual(history[-1]["id"], self.last_operation()["id"])
        dropped = [e for e in manifest["omitted"] if isinstance(e, dict) and "earlier_operations" in e]
        self.assertEqual(dropped[0]["earlier_operations"], 22 - len(history))
        self.assertEqual(selected["omitted"], manifest["omitted"])
        self.assertEqual(await self.propose("read_corpus", entry_id=self.source), "applied")
        self.assertEqual(self.s.verify(), [])

    async def test_oversized_legacy_metadata_cannot_stall_history(self):
        await self.steps(1)
        # A store predating the label bound may hold an artifact with a 12000-character title.
        with self.s.transaction():
            ref = self.s.create_artifact("T" * 11000, "theory", "short", self.s.working()["id"],
                                         {"invocation": self.last_operation()["invocation"], "actor": "legacy"})
        for _ in range(5):
            self.assertEqual(await self.propose("read_artifact", artifact_id=ref["id"], version=1), "applied")
        _, manifest, compiled = compile_context(self.s)
        self.assertLessEqual(len(compiled), self.s.config.input_chars)
        for entry in json.loads(compiled)["operation_history"]:
            if entry["name"] == "read_artifact":
                self.assertLessEqual(len(entry["result"]["title"]), 200)
        self.r.command("summon", body="still awake")
        self.assertEqual(await self.propose("read_artifact", artifact_id=ref["id"], version=1), "applied")
        self.assertEqual(self.s.verify(), [])


class FakeBlock:
    def __init__(self, type, **fields):
        self.type = type
        self.__dict__.update(fields)


class FakeResponse:
    def __init__(self, text, stop_reason="end_turn", model="claude-opus-5", stop_details=None):
        self.content = [FakeBlock("thinking", thinking=""), FakeBlock("text", text=text)]
        self.stop_reason, self.model, self.stop_details = stop_reason, model, stop_details
        self.usage = SimpleNamespace(input_tokens=1200, output_tokens=80, cache_creation_input_tokens=0, cache_read_input_tokens=0)
        self._request_id = "req_test"


class FakeClient:
    """Stands in for anthropic.AsyncAnthropic; records the request and returns a canned response."""
    def __init__(self, response):
        self.calls = []
        self.beta = SimpleNamespace(messages=SimpleNamespace(create=self.create))
        self.response = response

    async def create(self, **params):
        self.calls.append(params)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


class LiveAdapterTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cme-live-")
        self.path = Path(self.temp.name) / "state"
        self.s = initialize(self.path, ROOT / "demo/live-config.json")
        self.s.import_corpus("fixture", (ROOT / "demo/fixtures/margin.md").read_text())

    async def asyncTearDown(self):
        self.s.close()
        self.temp.cleanup()

    async def test_request_shape_reply_and_usage_unit(self):
        from chaos_magick_engine.live import ClaudeAdapter, SYSTEM
        raw = encode({"intent": "begin", "operation": {"name": "begin_working", "arguments": {
            "question": "Who owns a margin?", "intended_product": "a transmission", "motivation": "test"}}})
        client = FakeClient(FakeResponse(raw))
        r = Runtime(self.s, ClaudeAdapter(model="claude-opus-5", effort="medium", client=client))
        self.assertEqual(await r.step(), "applied")
        params = client.calls[0]
        self.assertEqual(params["model"], "claude-opus-5")
        self.assertEqual(params["system"], SYSTEM)
        self.assertEqual(params["output_config"], {"effort": "medium"})
        self.assertEqual(params["fallbacks"], "default")
        self.assertIn("server-side-fallback-2026-07-01", params["betas"])
        self.assertEqual(json.loads(params["messages"][0]["content"])["role"], "demon")
        inv = self.s.one("SELECT * FROM invocations")
        self.assertEqual(inv["raw"], raw)
        self.assertEqual(inv["usage"], len(inv["input"]) + len(raw))
        metadata = json.loads(inv["metadata"])
        self.assertFalse(metadata["synthetic"])
        self.assertEqual(metadata["tokens"]["input_tokens"], 1200)
        self.assertEqual(metadata["request_id"], "req_test")
        self.assertIsNotNone(self.s.working())
        self.assertEqual(self.s.verify(), [])
        await r.close()

    async def test_refusal_and_provider_error_are_explicit_outcomes(self):
        from chaos_magick_engine.live import ClaudeAdapter
        refused = FakeResponse("", stop_reason="refusal", stop_details=SimpleNamespace(category="test", explanation="x"))
        r = Runtime(self.s, ClaudeAdapter(client=FakeClient(refused)))
        self.assertEqual(await r.step(), "invalid")
        inv = self.s.one("SELECT * FROM invocations ORDER BY rowid DESC LIMIT 1")
        self.assertEqual(json.loads(inv["metadata"])["stop_details"]["category"], "test")
        self.assertIsNone(self.s.working())
        r.adapter = ClaudeAdapter(client=FakeClient(ConnectionError("synthetic outage")))
        r.command("run")
        self.assertEqual(await r.step(), "error")
        inv = self.s.one("SELECT * FROM invocations ORDER BY rowid DESC LIMIT 1")
        self.assertEqual(inv["status"], "error")
        self.assertGreater(inv["reservation"], 0)  # Unknown usage stays reserved.
        self.assertEqual(self.s.verify(), [])
        await r.close()

    async def test_overlong_reply_is_rejected_whole_with_metadata_kept(self):
        from chaos_magick_engine.live import ClaudeAdapter
        long_raw = encode({"intent": "x", "operation": {"name": "write_artifact", "arguments": {
            "title": "t", "kind": "theory", "content": "z" * (self.s.config.output_chars + 100), "source_refs": [], "parent_refs": []}}})
        r = Runtime(self.s, ClaudeAdapter(client=FakeClient(FakeResponse(long_raw))))
        self.assertEqual(await r.step(), "invalid")
        inv = self.s.one("SELECT * FROM invocations")
        self.assertEqual(inv["status"], "invalid")
        self.assertEqual(inv["usage"], len(inv["input"]) + len(long_raw))  # Honest overrun is spent, not hidden.
        self.assertEqual(inv["reservation"], 0)
        self.assertEqual(json.loads(inv["metadata"])["tokens"]["output_tokens"], 80)
        self.assertIn("output character bound", self.s.one("SELECT error FROM operations")["error"])
        self.assertIn(str(self.s.config.output_chars), json.loads(compile_context(self.s)[2])["reply_bound"])
        self.assertEqual(self.s.verify(), [])
        await r.close()

    async def test_no_fallbacks_and_key_file(self):
        from chaos_magick_engine.live import ClaudeAdapter, read_key
        adapter = ClaudeAdapter(fallbacks=False, client=FakeClient(FakeResponse("{}")))
        params = adapter.build(SimpleNamespace(invocation_id="i", command_epoch=0, compiled="{}", max_output_chars=10))
        self.assertNotIn("fallbacks", params)
        self.assertNotIn("betas", params)
        key = Path(self.temp.name) / "k"
        key.write_text("sk-test\n")
        self.assertEqual(read_key(key), "sk-test")
        key.write_text(" \n")
        with self.assertRaises(ValueError):
            read_key(key)


class FakeOpenAIResponse:
    def __init__(self, text, refusal=None, service_tier="flex", status="completed", incomplete=None):
        content = [FakeBlock("output_text", text=text)] if refusal is None else [FakeBlock("refusal", refusal=refusal)]
        self.output = [FakeBlock("reasoning"), FakeBlock("message", content=content)]
        self.id, self.model, self.service_tier, self.status = "resp_test", "gpt-5.6-sol", service_tier, status
        self.incomplete_details = None if incomplete is None else SimpleNamespace(reason=incomplete)
        self.usage = SimpleNamespace(input_tokens=1500, output_tokens=900,
                                     input_tokens_details=SimpleNamespace(cached_tokens=1024),
                                     output_tokens_details=SimpleNamespace(reasoning_tokens=700))
        self._request_id = "req_openai_test"


class RateLimitError(Exception):
    """Same name as the SDK's exception; the adapter matches by name so the tests need no SDK."""


class FakeOpenAIClient:
    """Stands in for openai.AsyncOpenAI; returns canned responses or exceptions in order."""
    def __init__(self, *responses):
        self.calls = []
        self.responses = list(responses)
        self.responses_api = SimpleNamespace(create=self.create)

    @property
    def responses(self):
        return self.responses_api

    @responses.setter
    def responses(self, value):
        self.queue = value

    async def create(self, **params):
        self.calls.append(params)
        response = self.queue.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


class OpenAIAdapterTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cme-openai-")
        self.path = Path(self.temp.name) / "state"
        self.s = initialize(self.path, ROOT / "demo/live-config.json")
        self.s.import_corpus("fixture", (ROOT / "demo/fixtures/margin.md").read_text())

    async def asyncTearDown(self):
        self.s.close()
        self.temp.cleanup()

    async def test_request_shape_reply_and_usage_unit(self):
        from chaos_magick_engine.live import OpenAIAdapter, SYSTEM
        raw = encode({"intent": "begin", "operation": {"name": "begin_working", "arguments": {
            "question": "Who owns a margin?", "intended_product": "a transmission", "motivation": "test"}}})
        client = FakeOpenAIClient(FakeOpenAIResponse(raw))
        r = Runtime(self.s, OpenAIAdapter(effort="xhigh", client=client))
        self.assertEqual(await r.step(), "applied")
        params = client.calls[0]
        self.assertEqual(params["model"], "gpt-5.6-sol")
        self.assertEqual(params["instructions"], SYSTEM)
        self.assertEqual(params["reasoning"], {"effort": "xhigh"})
        self.assertEqual(params["service_tier"], "flex")
        self.assertFalse(params["store"])
        self.assertEqual(json.loads(params["input"])["role"], "demon")
        inv = self.s.one("SELECT * FROM invocations")
        self.assertEqual(inv["raw"], raw)
        self.assertEqual(inv["usage"], len(inv["input"]) + len(raw))
        metadata = json.loads(inv["metadata"])
        self.assertEqual(metadata["provider"], "openai")
        self.assertFalse(metadata["synthetic"])
        self.assertEqual(metadata["tokens"], {"input_tokens": 1500, "output_tokens": 900, "cached_tokens": 1024, "reasoning_tokens": 700})
        self.assertEqual((metadata["requested_service_tier"], metadata["service_tier"]), ("flex", "flex"))
        self.assertEqual(metadata["request_id"], "req_openai_test")
        self.assertEqual(metadata["fallbacks"], [])
        self.assertIsNotNone(self.s.working())
        self.assertEqual(self.s.verify(), [])
        await r.close()

    async def test_refusal_capacity_fallback_and_provider_error(self):
        from chaos_magick_engine.live import OpenAIAdapter
        r = Runtime(self.s, OpenAIAdapter(client=FakeOpenAIClient(FakeOpenAIResponse("", refusal="declined"))))
        self.assertEqual(await r.step(), "invalid")
        inv = self.s.one("SELECT * FROM invocations ORDER BY rowid DESC LIMIT 1")
        self.assertEqual(json.loads(inv["metadata"])["stop_details"], {"category": "refusal", "explanation": "declined"})
        self.assertIsNone(self.s.working())
        # Flex capacity refused: the same request is re-issued once on the standard tier and recorded.
        raw = encode({"intent": "begin", "operation": {"name": "begin_working", "arguments": {
            "question": "Who owns a margin?", "intended_product": "a transmission", "motivation": "test"}}})
        client = FakeOpenAIClient(RateLimitError("resource_unavailable"), FakeOpenAIResponse(raw, service_tier="default"))
        r.adapter = OpenAIAdapter(client=client)
        r.command("run")
        self.assertEqual(await r.step(), "applied")
        self.assertEqual([c["service_tier"] for c in client.calls], ["flex", "auto"])
        metadata = json.loads(self.s.one("SELECT metadata FROM invocations ORDER BY rowid DESC LIMIT 1")["metadata"])
        self.assertEqual(metadata["fallbacks"][0]["from"], "flex")
        self.assertEqual(metadata["fallbacks"][0]["to"], "auto")
        self.assertEqual(metadata["service_tier"], "default")
        # Without fallbacks a capacity refusal is an explicit provider error with the reservation kept.
        r.adapter = OpenAIAdapter(fallbacks=False, client=FakeOpenAIClient(RateLimitError("resource_unavailable")))
        self.assertEqual(await r.step(), "error")
        inv = self.s.one("SELECT * FROM invocations ORDER BY rowid DESC LIMIT 1")
        self.assertEqual(inv["status"], "error")
        self.assertGreater(inv["reservation"], 0)
        # An incomplete reply is delivered as returned and its reason recorded; the engine judges it.
        r.adapter = OpenAIAdapter(client=FakeOpenAIClient(FakeOpenAIResponse("{\"intent\": \"cut", incomplete="max_output_tokens")))
        self.assertEqual(await r.step(), "invalid")
        metadata = json.loads(self.s.one("SELECT metadata FROM invocations ORDER BY rowid DESC LIMIT 1")["metadata"])
        self.assertEqual(metadata["incomplete_reason"], "max_output_tokens")
        self.assertEqual(self.s.verify(), [])
        await r.close()

    def test_console_builds_a_split_provider_router(self):
        demon_key, examiner_key = Path(self.temp.name) / "openai.key", Path(self.temp.name) / "anthropic.key"
        demon_key.write_text("sk-openai-test\n")
        examiner_key.write_text("sk-ant-test\n")
        args = SimpleNamespace(adapter="openai", model=None, effort="high", service_tier="flex", no_fallbacks=False,
                               timeout=None, key_file=str(demon_key), examiner_adapter="claude", examiner_model=None,
                               examiner_effort=None, examiner_key_file=str(examiner_key))
        router = adapter_for(args)
        self.assertIsInstance(router, RoleRouter)
        self.assertEqual((router.demon.model, router.demon.service_tier, router.demon.effort), ("gpt-5.6-sol", "flex", "high"))
        self.assertEqual((router.examiner.model, router.examiner.effort), ("claude-opus-5", "high"))
        self.assertEqual(router.demon.client.api_key, "sk-openai-test")
        self.assertEqual(router.examiner.client.api_key, "sk-ant-test")
        # One provider for both roles with no examiner settings is a single adapter, not a router.
        args.examiner_adapter, args.examiner_key_file = None, None
        self.assertNotIsInstance(adapter_for(args), RoleRouter)


class SubprocessTests(unittest.TestCase):
    def test_console_works_for_long_state_directory_paths(self):
        with tempfile.TemporaryDirectory(prefix="cme-long-") as temp:
            path = Path(temp) / ("deep-" * 25) / "state"
            self.assertGreater(len(str(path)), 108)
            s = initialize(path, ROOT / "demo/config.json")
            s.close()
            program = """
import asyncio, sys
from chaos_magick_engine.runtime import Runtime
from chaos_magick_engine.store import Store
s = Store(sys.argv[1])
async def main():
    r = Runtime(s)
    await r.start()
    print("READY", flush=True)
    await r.stop.wait()
    await r.close()
asyncio.run(main())
s.close()
"""
            child = subprocess.Popen([sys.executable, "-c", program, str(path)], cwd=ROOT,
                                     text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                self.assertEqual(child.stdout.readline().strip(), "READY")
                inspect = subprocess.run([sys.executable, "-m", "chaos_magick_engine", "--state-dir", str(path), "inspect"],
                                         cwd=ROOT, capture_output=True, text=True, timeout=5)
                self.assertEqual(inspect.returncode, 0, inspect.stderr)
                self.assertEqual(json.loads(inspect.stdout)["identity"]["lifecycle"], "active")
                shutdown = subprocess.run([sys.executable, "-m", "chaos_magick_engine", "--state-dir", str(path), "shutdown"],
                                          cwd=ROOT, capture_output=True, text=True, timeout=5)
                self.assertEqual(shutdown.returncode, 0, shutdown.stderr)
                _, stderr = child.communicate(timeout=5)
                self.assertEqual(child.returncode, 0, stderr)
                self.assertFalse((path / "control.sock").exists())
            finally:
                if child.poll() is None:
                    child.kill()
                    child.communicate()

    def test_demo_real_process_restart(self):
        with tempfile.TemporaryDirectory(prefix="cme-demo-") as temp:
            path = Path(temp) / "state"
            result = demonstration(path)
            self.assertEqual(result["issues"], [])
            report = json.loads(Path(result["details"]).read_text())
            self.assertTrue(report["same_identity_and_working_across_subprocesses"])
            self.assertTrue(report["interruption"]["receipt_before_provider_finished"])
            self.assertEqual(report["operations"].count("begin_working"), 1)
            self.assertEqual(report["operations"].count("write_artifact"), 1)
            self.assertIn("assimilate", report["operations"])
            self.assertFalse(report["live_model_instantiated"])
            with self.assertRaises(Invalid):
                demonstration(path)

    def test_uncertain_process_death_preserves_reservation(self):
        with tempfile.TemporaryDirectory(prefix="cme-crash-") as temp:
            path = Path(temp) / "state"
            s = initialize(path, ROOT / "demo/config.json")
            identity = s.identity()["id"]
            s.close()
            # Kill from inside the provider: invocation and reservation have already committed.
            program = '''
import asyncio, os, sys
from chaos_magick_engine.runtime import Runtime
from chaos_magick_engine.store import Store
class Dies:
    async def invoke(self, request):
        os._exit(73)
s = Store(sys.argv[1])
asyncio.run(Runtime(s, Dies()).step())
'''
            result = subprocess.run([sys.executable, "-c", program, str(path)], cwd=ROOT, timeout=5)
            self.assertEqual(result.returncode, 73)
            s = Store(path)
            try:
                Runtime(s)
                self.assertEqual(s.identity()["id"], identity)
                self.assertEqual(s.one("SELECT status FROM invocations")["status"], "uncertain")
                self.assertEqual(s.one("SELECT status FROM operations")["status"], "uncertain")
                self.assertGreater(s.one("SELECT * FROM allocation")["reserved"], 0)
                self.assertEqual(s.one("SELECT * FROM allocation")["calls"], 1)
                self.assertEqual(s.verify(), [])
            finally:
                s.close()

    def test_process_crashes_on_both_local_commit_boundaries(self):
        for boundary in ("before_commit", "after_commit"):
            with self.subTest(boundary=boundary), tempfile.TemporaryDirectory(prefix="cme-commit-") as temp:
                path = Path(temp) / "state"
                s = initialize(path, ROOT / "demo/config.json")
                s.import_corpus("fixture", (ROOT / "demo/fixtures/margin.md").read_text())
                identity = s.identity()["id"]
                s.close()
                program = """
import asyncio, os, sys
from chaos_magick_engine.runtime import Runtime
from chaos_magick_engine.store import Store
s = Store(sys.argv[1])
r = Runtime(s)
async def main():
    for _ in range(4):
        assert await r.step() == "applied"
    def crash(boundary):
        if boundary == sys.argv[2]:
            os._exit(74)
    r.faculties.crash_hook = crash
    await r.step()
asyncio.run(main())
"""
                result = subprocess.run([sys.executable, "-c", program, str(path), boundary], cwd=ROOT, timeout=5)
                self.assertEqual(result.returncode, 74)
                s = Store(path)
                try:
                    Runtime(s)
                    self.assertEqual(s.identity()["id"], identity)
                    products = s.rows("SELECT * FROM artifacts WHERE kind='transmission'")
                    self.assertEqual(len(products), 1)
                    op = s.one("SELECT * FROM operations ORDER BY rowid DESC LIMIT 1")
                    self.assertEqual(op["status"], "committed")
                    from chaos_magick_engine.faculties import Faculties
                    Faculties(s).apply(op["id"])
                    self.assertEqual(len(s.rows("SELECT * FROM versions WHERE artifact_id=?", (products[0]["id"],))), 1)
                    self.assertEqual(s.one("SELECT * FROM allocation")["calls"], 5)
                    self.assertEqual(s.verify(), [])
                finally:
                    s.close()

    def test_console_shutdown_terminates_cancellation_resistant_process(self):
        import select
        with tempfile.TemporaryDirectory(prefix="cme-stop-") as temp:
            path = Path(temp) / "state"
            s = initialize(path, ROOT / "demo/config.json")
            s.close()
            program = """
import asyncio, sys
from types import SimpleNamespace
import chaos_magick_engine.runtime as module
from chaos_magick_engine.__main__ import bounded_loop, run_async
from chaos_magick_engine.store import Store
class Forever:
    async def invoke(self, request):
        print("BLOCKED", flush=True)
        while True:
            try:
                await asyncio.Event().wait()
            except asyncio.CancelledError:
                pass
module.ScriptedAdapter = Forever
s = Store(sys.argv[1])
try:
    bounded_loop(run_async(s, SimpleNamespace(once=False, steps=None)))
finally:
    s.close()
"""
            child = subprocess.Popen([sys.executable, "-c", program, str(path)], cwd=ROOT,
                                     text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                readable, _, _ = select.select([child.stdout], [], [], 3)
                self.assertTrue(readable, "provider barrier not reached")
                self.assertEqual(child.stdout.readline().strip(), "BLOCKED")
                command = subprocess.run([sys.executable, "-m", "chaos_magick_engine", "--state-dir", str(path), "shutdown"],
                                         cwd=ROOT, capture_output=True, text=True, timeout=2)
                self.assertEqual(command.returncode, 0, command.stderr)
                _, stderr = child.communicate(timeout=2)
                self.assertEqual(child.returncode, 0, stderr)
                s = Store(path)
                try:
                    self.assertEqual(s.one("SELECT status FROM invocations")["status"], "unresolved")
                    self.assertGreater(s.one("SELECT * FROM allocation")["reserved"], 0)
                    self.assertEqual(s.verify(), [])
                finally:
                    s.close()
            finally:
                if child.poll() is None:
                    child.kill()
                    child.communicate()

    def test_init_refuses_existing_identity_and_unknown_schema(self):
        with tempfile.TemporaryDirectory(prefix="cme-schema-") as temp:
            path = Path(temp) / "state"
            s = initialize(path, ROOT / "demo/config.json")
            identity = s.identity()["id"]
            s.close()
            with self.assertRaisesRegex(Invalid, "already initialized"):
                initialize(path, ROOT / "demo/config.json")
            s = Store(path)
            self.assertEqual(s.identity()["id"], identity)
            s.db.execute("PRAGMA user_version=99")
            s.close()
            with self.assertRaisesRegex(Invalid, "unsupported schema"):
                Store(path)


if __name__ == "__main__":
    unittest.main()
