"""Local effects: validation and completion share one rollback boundary."""
import json

from .domain import CONTRACTS, Invalid, KINDS, PHASES, assessment, fields, parse, proposal, require
from .store import encode, uid


class Faculties:
    def __init__(self, store):
        self.s = store
        self.crash_hook = lambda boundary: None

    def apply(self, operation_id):
        s = self.s
        op = s.one("SELECT * FROM operations WHERE id=?", (operation_id,))
        require(op is not None, "unknown engine operation ID")
        if op["status"] == "committed":
            return json.loads(op["result"])
        require(op["status"] == "pending", "operation cannot be replayed")
        inv = s.one("SELECT * FROM invocations WHERE id=?", (op["invocation"],))
        try:
            with s.transaction():
                identity = s.identity()
                require(inv["epoch"] == identity["epoch"] and inv["revision"] == identity["revision"]
                        and identity["lifecycle"] == "active", "stale invocation precondition")
                working = s.working()
                if inv["role"] == "examiner":
                    require(working and working["phase"] == "examination", "examination not pending")
                    value = assessment(inv["raw"], s.config.output_chars)
                    require(value["examined_refs"] == working["data"]["products"], "examiner reference mismatch")
                    result = s.create_artifact("Assessment", "assessment", encode(value), working["id"],
                                               {"invocation": inv["id"], "actor": "examiner", "synthetic": True},
                                               parents=value["examined_refs"])
                    working["data"]["assessment"] = result
                    working["data"]["assimilated"] = False
                    working["phase"] = "assimilation"
                    name = "examine"
                else:
                    value = proposal(inv["raw"], s.config.output_chars)
                    name = value["operation"]["name"]
                    args = value["operation"]["arguments"]
                    phase = working["phase"] if working else None
                    require(phase in PHASES[name], f"{name} illegal in {phase}")
                    result, working = self.execute(name, args, working, inv)
                if working:
                    s.db.execute("UPDATE workings SET phase=?,status=?,revision=revision+1,data=? WHERE id=?",
                                 (working["phase"], working["status"], encode(working["data"]), working["id"]))
                s.db.execute("UPDATE identity SET revision=revision+1")
                s.db.execute("UPDATE operations SET status='committed',proposal=?,result=? WHERE id=?",
                             (encode(value), encode(result), operation_id))
                s.db.execute("UPDATE invocations SET status='applied' WHERE id=?", (inv["id"],))
                s.event(name, {"result": result, "invocation": inv["id"]}, operation_id,
                        actor="examiner" if name == "examine" else s.identity()["id"])
                self.crash_hook("before_commit")
            self.crash_hook("after_commit")
            return result
        except Invalid as exc:
            with s.transaction():
                s.db.execute("UPDATE operations SET status='rejected',error=? WHERE id=?", (str(exc), operation_id))
                s.db.execute("UPDATE invocations SET status='invalid' WHERE id=?", (inv["id"],))
                s.event("validation_rejected", {"operation": operation_id, "error": str(exc)})
            raise

    def frame_content(self, content):
        frame = parse(content, self.s.config.output_chars)
        fields(frame, CONTRACTS["define_frame"])
        for key, validator in CONTRACTS["define_frame"].items():
            validator(frame[key])

    def execute(self, name, a, w, inv):
        s = self.s
        d = w["data"] if w else None
        provenance = {"invocation": inv["id"], "actor": s.identity()["id"], "synthetic": True,
                      "feedback_ids": [row["id"] for row in json.loads(inv["input"]).get("operator_feedback", [])]}
        if name == "begin_working":
            w = {"id": uid(), "phase": "orientation", "status": "unfinished",
                 "data": {**a, "frames": [], "products": [], "read_sources": [], "segment": 0,
                          "active_frame": None, "unresolved_questions": []}}
            s.db.execute("INSERT INTO workings VALUES(?,?,?,0,?)",
                         (w["id"], w["phase"], w["status"], encode(w["data"])))
            s.db.execute("UPDATE identity SET selected=?", (w["id"],))
            return {"working_id": w["id"]}, w
        if name == "select_working":
            target = s.one("SELECT * FROM workings WHERE id=?", (a["working_id"],))
            require(target is not None, "working unavailable")
            require(target["status"] not in ("completed", "abandoned"), "terminal working cannot reopen")
            target["data"] = json.loads(target["data"])
            if target["status"] == "deferred":
                target["phase"] = "orientation"
            target["status"] = "unfinished"
            s.db.execute("UPDATE identity SET selected=?", (target["id"],))
            return {"working_id": target["id"]}, target
        if name == "read_corpus":
            row = s.one("SELECT * FROM corpus WHERE id=?", (a["entry_id"],))
            require(row is not None, "corpus unavailable")
            if d is not None and row["id"] not in d["read_sources"]:
                d["read_sources"].append(row["id"])
            # The result records what was read; content reaches the model once through
            # read_material, instead of being copied into every later compiled history.
            return {"id": row["id"], "source": row["source"], "hash": row["hash"],
                    "version": 1, "chars": len(row["content"])}, w
        if name == "read_artifact":
            return s.artifact({"id": a["artifact_id"], "version": a["version"]}), w
        if name == "define_frame":
            ref = s.create_artifact(a["name"], "frame", encode(a), w["id"], provenance)
            d["frames"].append(ref)
            return ref, w
        if name == "enter_frame":
            ref = {"id": a["frame_id"], "version": a["version"]}
            frame = s.artifact(ref)
            require(frame["kind"] == "frame" and frame["working"] == w["id"] and ref in d["frames"],
                    "frame not defined for this working")
            require(not d["active_frame"], "already exploring")
            if w["phase"] == "assimilation":
                require(d.get("assimilated"), "assimilate assessment before next segment")
            d["active_frame"] = ref
            d["segment"] += 1
            d["products"] = []
            d.pop("assessment", None)
            w["phase"] = "exploration"
            return {"frame": ref, "segment": d["segment"]}, w
        if name == "write_artifact":
            require(a["kind"] in KINDS, "unknown artifact kind")
            if a["kind"] == "frame":
                self.frame_content(a["content"])
            s.check_refs(a["source_refs"], sources=True)
            s.check_refs(a["parent_refs"])
            ref = s.create_artifact(a["title"], a["kind"], a["content"], w["id"], provenance,
                                    a["parent_refs"], a["source_refs"], frame=d["active_frame"], segment=d["segment"])
            if a["kind"] == "frame":
                d["frames"].append(ref)
            return ref, w
        if name == "revise_artifact":
            ref = {"id": a["artifact_id"], "version": a["expected_version"]}
            old = s.artifact(ref)
            require(old["working"] == w["id"] and old["kind"] in KINDS,
                    "cannot revise protected artifact or another working's artifact")
            if old["kind"] == "frame":
                self.frame_content(a["content"])
            latest = s.one("SELECT MAX(version) n FROM versions WHERE artifact_id=?", (a["artifact_id"],))["n"]
            require(latest == a["expected_version"], "version precondition failed")
            sources = [{"id": r["corpus_id"], "version": 1} for r in s.rows(
                "SELECT corpus_id FROM source_links WHERE artifact_id=? AND version=?", (ref["id"], ref["version"]))]
            sources += [{"id": r["target_id"], "version": r["target_version"]} for r in s.rows(
                "SELECT * FROM links WHERE artifact_id=? AND version=? AND relation='source'", (ref["id"], ref["version"]))]
            new_ref = s.add_version(ref["id"], a["content"], {**provenance, "change_note": a["change_note"]}, [ref], sources)
            if old["kind"] == "frame":
                d["frames"].append(new_ref)
            return new_ref, w
        if name == "leave_frame":
            require(bool(a["product_refs"]), "examination needs products")
            s.check_refs(a["product_refs"])
            for ref in a["product_refs"]:
                product = s.artifact(ref)
                require(product["working"] == w["id"] and product["segment"] == d["segment"]
                        and product["kind"] != "frame", "product outside active segment")
            d["products"] = a["product_refs"]
            d["extraction_note"] = a["extraction_note"]
            d.setdefault("segments", []).append({"frame": d["active_frame"], "products": a["product_refs"],
                                                  "extraction_note": a["extraction_note"], "segment": d["segment"]})
            d["active_frame"] = None
            w["phase"] = "examination"
            return {"examination": "queued", "products": d["products"]}, w
        if name == "assimilate":
            require(a["assessment_ref"] == d.get("assessment") and not d.get("assimilated"),
                    "assessment unavailable or already assimilated")
            s.artifact(a["assessment_ref"])
            parents = [a["assessment_ref"]] + d["products"]
            previous = s.identity()["self_account"]
            if previous:
                parents.append(json.loads(previous))
            ref = s.create_artifact("Self-account", "self_account", a["self_account_change"], w["id"],
                                    provenance, parents=parents)
            s.db.execute("UPDATE identity SET self_account=?,commitments=?,next_pursuit=?",
                         (encode(ref), encode(a["doctrine_changes"]), a["next_pursuit"]))
            d["assimilated"] = True
            return {"self_account": ref, "next_pursuit": a["next_pursuit"]}, w
        if name == "finish_working":
            require(a["outcome"] in ("completed", "abandoned", "deferred"), "invalid outcome")
            s.check_refs(a["product_refs"])
            require(all(s.artifact(r)["working"] == w["id"] for r in a["product_refs"]), "foreign product")
            if a["outcome"] == "completed":
                require(w["phase"] == "assimilation" and d.get("assimilated"), "completion needs assimilation")
            if d["active_frame"]:
                d.setdefault("segments", []).append({"frame": d["active_frame"], "products": a["product_refs"],
                                                      "outcome": a["outcome"], "segment": d["segment"]})
            d["active_frame"] = None
            d["unresolved_questions"] = a["unresolved_questions"]
            d["final_products"] = a["product_refs"]
            w["phase"], w["status"] = "settled", a["outcome"]
            return {"outcome": a["outcome"]}, w
        if name == "wait":
            from .domain import fields, string
            condition = a["wake_condition"]
            require(type(condition) is dict, "invalid wake condition")
            if condition.get("kind") == "timer":
                fields(condition, ("kind", "at"))
                import math
                require(type(condition["at"]) in (int, float) and math.isfinite(condition["at"])
                        and condition["at"] > s.clock(), "timer must be finite and in the future")
            else:
                fields(condition, ("kind", "event"))
                require(condition["kind"] == "event" and condition["event"] == "operator", "unsupported wake")
            string(a["reason"])
            s.db.execute("UPDATE identity SET wake=?", (encode({"condition": condition, "reason": a["reason"]}),))
            if w and w["status"] == "unfinished":
                w["status"] = "waiting"
            return {"waiting": condition}, w
        raise Invalid("faculty not implemented")
