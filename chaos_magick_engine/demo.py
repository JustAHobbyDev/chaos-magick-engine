"""Reproducible subprocess restart plus barrier-controlled real console interruption."""
import asyncio
import json
from pathlib import Path
import subprocess
import sys

from .adapters import BarrierAdapter
from .domain import require
from .runtime import Runtime, send
from .store import Store


async def interrupt(directory):
    s = Store(directory)
    adapter = BarrierAdapter()
    runtime = Runtime(s, adapter)
    await runtime.start()
    runtime.command("summon", body="Synthetic interruption probe")
    step = asyncio.create_task(runtime.step())
    try:
        await asyncio.wait_for(adapter.started.wait(), 2)
        before = len(s.rows("SELECT * FROM versions"))
        receipt = await asyncio.wait_for(send(directory, "suspend"), 2)
        require(not adapter.finished.is_set(), "receipt waited for blocked provider")
        adapter.release.set()
        outcome = await asyncio.wait_for(step, 2)
        require(outcome == "superseded", "stale response was not suppressed")
        require(len(s.rows("SELECT * FROM versions")) == before, "stale action had effects")
        runtime.command("restore")
        return {"receipt_before_provider_finished": True, "receipt": receipt, "late_response": outcome}
    finally:
        adapter.release.set()
        await runtime.close()
        s.close()


def demonstration(directory):
    from .__main__ import ROOT, export
    directory = Path(directory).resolve()
    require(not directory.exists() or not any(directory.iterdir()), "demo needs an empty directory; refusing to wipe existing files")
    commands = []
    def run(*args):
        command = [sys.executable, "-m", "chaos_magick_engine", "--state-dir", str(directory), *args]
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=20)
        require(result.returncode == 0, result.stderr)
        commands.append({"argv": command, "returncode": result.returncode, "stdout": result.stdout.strip()})
        return json.loads(result.stdout)
    first = run("init")
    run("import-corpus", str(ROOT / "demo/fixtures/margin.md"))
    run("run", "--once", "--steps", "5")
    before = run("inspect")
    require(before["working"]["phase"] == "exploration", "restart checkpoint is not mid-working")
    run("run", "--once")
    after = run("inspect")
    require(after["identity"]["id"] == first["identity_id"], "identity changed on restart")
    require(before["working"]["id"] == after["working"]["id"], "working changed on restart")
    require(after["working"]["data"]["assimilated"], "cycle did not reach assimilation")
    race = asyncio.run(interrupt(directory))
    verification = run("verify")
    s = Store(directory)
    try:
        paths = export(s, directory / "exports")
        report = {"synthetic_content": True, "live_model_instantiated": False,
                  "identity_id": first["identity_id"], "working_id": after["working"]["id"],
                  "same_identity_and_working_across_subprocesses": True,
                  "working_status": after["working"]["status"], "next_pursuit": after["identity"]["next_pursuit"],
                  "interruption": race, "verification": verification, "exports": paths,
                  "operations": [r["kind"] for r in s.rows("SELECT kind FROM events WHERE operation_id IS NOT NULL ORDER BY seq")],
                  "commands_executed": commands}
        (directory / "execution-report.json").write_text(json.dumps(report, indent=2) + "\n")
        (directory / "execution-report.md").write_text(
            "# Persistent core offline execution\n\n"
            "Synthetic creative content and assessment; engine events were actually executed. "
            "No live model-backed demon was instantiated. No reception, remote effects, or creative improvement is established.\n\n"
            f"Identity: `{first['identity_id']}`. Same unfinished working resumed in a second subprocess.\n\n"
            f"Operations: {', '.join(report['operations'])}.\n\n"
            "Suspend receipt arrived through the Unix socket before a barrier-blocked adapter finished; "
            "its late proposal was superseded with no operation effect. Restore retained the identity.\n\n"
            f"Consistency issues: {verification['issues']}. Full command outputs: execution-report.json.\n")
        return {"report": str(directory / "execution-report.md"), "details": str(directory / "execution-report.json"),
                "exports": paths, "issues": verification["issues"]}
    finally:
        s.close()
