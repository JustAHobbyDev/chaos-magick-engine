"""Canonical SQLite state; explicitly autocommitted reads and IMMEDIATE writes."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import time
import uuid
from contextlib import contextmanager

from .domain import Config, Invalid, require


def uid():
    return uuid.uuid4().hex


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def digest(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def artifact_read_result(row):
    """Compact a full artifact row or an already compact read result."""
    return {**{key: row[key] for key in ("id", "version", "kind", "hash")}, "title": row["title"][:200],
            "chars": len(row["content"]) if "content" in row else row["chars"]}


SCHEMA = """
CREATE TABLE identity(id TEXT PRIMARY KEY, name TEXT NOT NULL, seed TEXT NOT NULL,
 seed_source TEXT NOT NULL, seed_hash TEXT NOT NULL, seed_version TEXT NOT NULL,
 lifecycle TEXT NOT NULL, epoch INTEGER NOT NULL, revision INTEGER NOT NULL,
 selected TEXT REFERENCES workings(id), self_account TEXT, commitments TEXT NOT NULL,
 next_pursuit TEXT NOT NULL, wake TEXT, config TEXT NOT NULL);
CREATE TABLE workings(id TEXT PRIMARY KEY, phase TEXT NOT NULL, status TEXT NOT NULL,
 revision INTEGER NOT NULL, data TEXT NOT NULL);
CREATE TABLE corpus(id TEXT PRIMARY KEY, source TEXT NOT NULL, content TEXT NOT NULL, hash TEXT NOT NULL);
CREATE TABLE artifacts(id TEXT PRIMARY KEY, title TEXT NOT NULL, kind TEXT NOT NULL,
 working TEXT REFERENCES workings(id), segment INTEGER, frame_id TEXT, frame_version INTEGER,
 FOREIGN KEY(frame_id,frame_version) REFERENCES versions(artifact_id,version));
CREATE TABLE versions(artifact_id TEXT REFERENCES artifacts(id), version INTEGER NOT NULL,
 content TEXT NOT NULL, hash TEXT NOT NULL, provenance TEXT NOT NULL,
 PRIMARY KEY(artifact_id,version));
CREATE TABLE links(artifact_id TEXT, version INTEGER, target_id TEXT, target_version INTEGER,
 relation TEXT NOT NULL, PRIMARY KEY(artifact_id,version,target_id,target_version,relation),
 FOREIGN KEY(artifact_id,version) REFERENCES versions(artifact_id,version),
 FOREIGN KEY(target_id,target_version) REFERENCES versions(artifact_id,version));
CREATE TABLE source_links(artifact_id TEXT, version INTEGER, corpus_id TEXT REFERENCES corpus(id),
 PRIMARY KEY(artifact_id,version,corpus_id),
 FOREIGN KEY(artifact_id,version) REFERENCES versions(artifact_id,version));
CREATE TABLE commands(id TEXT PRIMARY KEY, kind TEXT NOT NULL, scope TEXT NOT NULL,
 body TEXT NOT NULL, epoch INTEGER NOT NULL, status TEXT NOT NULL, receipt TEXT NOT NULL);
CREATE TABLE events(seq INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT UNIQUE NOT NULL,
 at REAL NOT NULL, actor TEXT NOT NULL, kind TEXT NOT NULL, data TEXT NOT NULL,
 operation_id TEXT UNIQUE REFERENCES operations(id));
CREATE TABLE invocations(id TEXT PRIMARY KEY, epoch INTEGER NOT NULL, revision INTEGER NOT NULL,
 role TEXT NOT NULL, manifest TEXT NOT NULL, input TEXT NOT NULL, raw TEXT,
 status TEXT NOT NULL, metadata TEXT NOT NULL, usage INTEGER, reservation INTEGER NOT NULL);
CREATE TABLE operations(id TEXT PRIMARY KEY, invocation TEXT UNIQUE REFERENCES invocations(id),
 status TEXT NOT NULL, proposal TEXT, result TEXT, error TEXT);
CREATE TABLE allocation(id INTEGER PRIMARY KEY CHECK(id=1), calls INTEGER NOT NULL,
 spent INTEGER NOT NULL, reserved INTEGER NOT NULL);
CREATE TABLE feedback(id TEXT PRIMARY KEY, artifact_id TEXT, version INTEGER,
 content TEXT NOT NULL, at REAL NOT NULL,
 FOREIGN KEY(artifact_id,version) REFERENCES versions(artifact_id,version));
CREATE TRIGGER immutable_versions_update BEFORE UPDATE ON versions BEGIN SELECT RAISE(ABORT,'immutable version'); END;
CREATE TRIGGER immutable_versions_delete BEFORE DELETE ON versions BEGIN SELECT RAISE(ABORT,'immutable version'); END;
CREATE TRIGGER immutable_events_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT,'append-only events'); END;
CREATE TRIGGER immutable_events_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT,'append-only events'); END;
CREATE TRIGGER immutable_corpus_update BEFORE UPDATE ON corpus BEGIN SELECT RAISE(ABORT,'immutable corpus'); END;
CREATE TRIGGER immutable_corpus_delete BEFORE DELETE ON corpus BEGIN SELECT RAISE(ABORT,'immutable corpus'); END;
PRAGMA user_version=1;
"""


class Store:
    def __init__(self, directory, *, initialize=False, config=None, seed=None, clock=time.time):
        self.path = Path(directory).resolve()
        self.clock = clock
        self.path.mkdir(mode=0o700, parents=True, exist_ok=True)
        require(self.path.stat().st_uid == os.getuid(), "state directory must belong to local account")
        os.chmod(self.path, 0o700)
        self.lock = open(self.path / "runner.lock", "a+b")
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.lock.close()
            raise Invalid("another runner owns this state store") from None
        self.db = None
        try:
            database = self.path / "engine.sqlite3"
            require(initialize or database.exists(), "store is not initialized")
            self.db = sqlite3.connect(database, isolation_level=None)
            self.db.row_factory = sqlite3.Row
            self.db.execute("PRAGMA foreign_keys=ON")
            self.db.execute("PRAGMA journal_mode=WAL")
            self.db.execute("PRAGMA synchronous=FULL")
            version = self.db.execute("PRAGMA user_version").fetchone()[0]
            require(version in (0, 1), f"unsupported schema version {version}")
            if version == 0:
                require(initialize and config is not None and seed is not None, "empty store needs init")
                require(not self.db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall(),
                        "refusing unrecognized nonempty database")
                self.db.executescript("BEGIN IMMEDIATE;\n" + SCHEMA)
                try:
                    self.db.execute("INSERT INTO identity VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                                    (uid(), "The Heresiarch", seed, "design/004-founding-demon.md#compact-invocation-seed",
                                     digest(seed), "0.2", "active", 0, 0, None, None, "[]", "", "initialization",
                                     encode(config.__dict__)))
                    self.db.execute("INSERT INTO allocation VALUES(1,0,0,0)")
                    self.event("initialized", {"development": True, "seed_hash": digest(seed)})
                    self.db.execute("COMMIT")
                except BaseException:
                    self.db.execute("ROLLBACK")
                    raise
            elif initialize:
                raise Invalid("already initialized; refusing to reseed")
            self.config = Config.from_dict(json.loads(self.identity()["config"]))
        except BaseException:
            self.close()
            raise

    def close(self):
        if self.db is not None:
            self.db.close()
            self.db = None
        if not self.lock.closed:
            self.lock.close()

    @contextmanager
    def transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def rows(self, sql, args=()):
        return [dict(row) for row in self.db.execute(sql, args)]

    def one(self, sql, args=()):
        row = self.db.execute(sql, args).fetchone()
        return dict(row) if row else None

    def identity(self):
        return self.one("SELECT * FROM identity")

    def working(self):
        selected = self.identity()["selected"]
        row = self.one("SELECT * FROM workings WHERE id=?", (selected,))
        if row:
            row["data"] = json.loads(row["data"])
        return row

    def event(self, kind, data, operation=None, actor="engine"):
        event_id = uid()
        self.db.execute("INSERT INTO events(id,at,actor,kind,data,operation_id) VALUES(?,?,?,?,?,?)",
                        (event_id, self.clock(), actor, kind, encode(data), operation))
        return event_id

    def artifact(self, ref):
        row = self.one("SELECT a.*,v.version,v.content,v.hash,v.provenance FROM artifacts a "
                       "JOIN versions v ON a.id=v.artifact_id WHERE a.id=? AND v.version=?",
                       (ref["id"], ref["version"]))
        require(row is not None, "artifact version unavailable")
        return row

    def check_refs(self, refs, *, sources=False):
        for ref in refs:
            if sources and self.one("SELECT id FROM corpus WHERE id=?", (ref["id"],)):
                require(ref["version"] == 1, "corpus version must be 1")
            else:
                self.artifact(ref)

    def create_artifact(self, title, kind, content, working, provenance, parents=(), sources=(),
                        artifact_id=None, frame=None, segment=None):
        artifact_id = artifact_id or uid()
        self.db.execute("INSERT INTO artifacts VALUES(?,?,?,?,?,?,?)",
                        (artifact_id, title, kind, working, segment,
                         frame["id"] if frame else None, frame["version"] if frame else None))
        return self.add_version(artifact_id, content, provenance, parents, sources)

    def add_version(self, artifact_id, content, provenance, parents=(), sources=()):
        version = self.db.execute("SELECT COALESCE(MAX(version),0)+1 FROM versions WHERE artifact_id=?",
                                  (artifact_id,)).fetchone()[0]
        self.db.execute("INSERT INTO versions VALUES(?,?,?,?,?)",
                        (artifact_id, version, content, digest(content), encode(provenance)))
        for ref in parents:
            self.db.execute("INSERT OR IGNORE INTO links VALUES(?,?,?,?,?)",
                            (artifact_id, version, ref["id"], ref["version"], "derives_from"))
        for ref in sources:
            if self.one("SELECT id FROM corpus WHERE id=?", (ref["id"],)):
                self.db.execute("INSERT OR IGNORE INTO source_links VALUES(?,?,?)",
                                (artifact_id, version, ref["id"]))
            else:
                self.db.execute("INSERT OR IGNORE INTO links VALUES(?,?,?,?,?)",
                                (artifact_id, version, ref["id"], ref["version"], "source"))
        return {"id": artifact_id, "version": version}

    def import_corpus(self, source, content):
        require(type(content) is str and bool(content), "empty corpus")
        with self.transaction():
            entry_id = uid()
            self.db.execute("INSERT INTO corpus VALUES(?,?,?,?)", (entry_id, source, content, digest(content)))
            self.event("corpus_imported", {"id": entry_id, "hash": digest(content), "source": source})
        return entry_id

    def recover(self):
        with self.transaction():
            rows = self.rows("SELECT id,status FROM invocations WHERE status IN ('running','timed_out','unresolved')")
            for row in rows:
                self.db.execute("UPDATE invocations SET status='uncertain' WHERE id=?", (row["id"],))
                self.db.execute("UPDATE operations SET status='uncertain' WHERE invocation=? AND status='pending'",
                                (row["id"],))
                self.event("invocation_uncertain", row)
            # Reservations remain charged; a lost response does not establish zero remote usage.
        return rows

    def inspect(self):
        return {"identity": self.identity(), "working": self.working(),
                "workings": self.rows("SELECT * FROM workings"),
                "allocation": self.one("SELECT * FROM allocation"),
                "commands": self.rows("SELECT * FROM commands"),
                "artifacts": self.rows("SELECT * FROM artifacts"),
                "invocations": self.rows("SELECT id,status,usage,reservation FROM invocations"),
                "operations": self.rows("SELECT * FROM operations"),
                "feedback": self.rows("SELECT * FROM feedback")}

    def verify(self):
        issues = [f"foreign key: {tuple(row)}" for row in self.db.execute("PRAGMA foreign_key_check")]
        if self.db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            issues.append("SQLite integrity failure")
        for table in ("corpus", "versions"):
            for row in self.rows(f"SELECT * FROM {table}"):
                if digest(row["content"]) != row["hash"]:
                    issues.append(f"{table} content hash mismatch")
        if digest(self.identity()["seed"]) != self.identity()["seed_hash"]:
            issues.append("seed hash mismatch")
        for row in self.rows("SELECT * FROM workings"):
            try:
                data = json.loads(row["data"])
            except ValueError:
                issues.append("invalid working data JSON")
                continue
            if (row["phase"] == "exploration") != bool(data.get("active_frame")):
                issues.append("invalid phase/frame combination")
            if row["phase"] not in {"orientation", "exploration", "examination", "assimilation", "settled"}:
                issues.append("unknown working phase")
            refs = (data.get("products", []) + data.get("frames", []) + data.get("final_products", [])
                    + data.get("read_artifacts", []))
            refs += [data[key] for key in ("assessment", "active_frame") if data.get(key)]
            for segment in data.get("segments", []):
                refs += segment.get("products", []) + [segment["frame"]]
            for ref in refs:
                try:
                    self.artifact(ref)
                except (Invalid, KeyError, TypeError):
                    issues.append("missing working reference")
            if data.get("active_frame"):
                try:
                    frame = self.artifact(data["active_frame"])
                    if frame["kind"] != "frame" or frame["working"] != row["id"] or data["active_frame"] not in data.get("frames", []):
                        issues.append("invalid active frame reference")
                except (Invalid, KeyError, TypeError):
                    issues.append("missing active frame")
            if row["status"] not in {"unfinished", "waiting", "completed", "abandoned", "deferred"}:
                issues.append("invalid working status")
            if (row["phase"] == "settled") != (row["status"] in {"completed", "abandoned", "deferred"}):
                issues.append("invalid settled status")
            for corpus_id in data.get("read_sources", []):
                if not self.one("SELECT id FROM corpus WHERE id=?", (corpus_id,)):
                    issues.append("missing working corpus")
            if row["phase"] == "examination" and not data.get("products"):
                issues.append("examination without products")
        for row in self.rows("SELECT o.*,e.id AS event_id,e.kind AS event_kind,e.data AS event_data FROM operations o LEFT JOIN events e ON e.operation_id=o.id"):
            if (row["status"] == "committed") != bool(row["event_id"]):
                issues.append("inconsistent operation/event")
            if row["status"] == "committed":
                try:
                    result, proposal = json.loads(row["result"]), json.loads(row["proposal"])
                    event = json.loads(row["event_data"])
                    name = proposal.get("operation", {}).get("name", "examine")
                    if event["result"] != result or event["invocation"] != row["invocation"] or name != row["event_kind"]:
                        issues.append("operation/event content mismatch")
                except (ValueError, KeyError, TypeError):
                    issues.append("committed operation missing result/event content")
        for row in self.rows("SELECT a.id FROM artifacts a LEFT JOIN versions v ON a.id=v.artifact_id WHERE v.artifact_id IS NULL"):
            issues.append(f"artifact without content: {row['id']}")
        for inv in self.rows("SELECT * FROM invocations"):
            try:
                manifest = json.loads(inv["manifest"])
                if digest(inv["input"]) != manifest["input_hash"] or len(inv["input"]) != manifest["input_chars"]:
                    issues.append("invocation input manifest mismatch")
            except (ValueError, KeyError, TypeError):
                issues.append("invalid invocation manifest")
        self_ref = self.identity()["self_account"]
        if self_ref:
            try:
                self.artifact(json.loads(self_ref))
            except (Invalid, ValueError, KeyError, TypeError):
                issues.append("missing self-account content")
        for version in self.rows("SELECT * FROM versions"):
            try:
                provenance = json.loads(version["provenance"])
                op = self.one("SELECT * FROM operations WHERE invocation=?", (provenance["invocation"],))
                if not op or op["status"] != "committed":
                    issues.append("artifact lacks committed provenance")
                for feedback_id in provenance.get("feedback_ids", []):
                    if not self.one("SELECT id FROM feedback WHERE id=?", (feedback_id,)):
                        issues.append("missing feedback provenance")
            except (ValueError, KeyError, TypeError):
                issues.append("invalid artifact provenance")
        alloc = self.one("SELECT * FROM allocation")
        totals = self.one("SELECT COUNT(*) calls,COALESCE(SUM(usage),0) spent,COALESCE(SUM(reservation),0) reserved FROM invocations")
        if any(alloc[key] != totals[key] for key in ("calls", "spent", "reserved")):
            issues.append("allocation ledger mismatch")
        return issues
