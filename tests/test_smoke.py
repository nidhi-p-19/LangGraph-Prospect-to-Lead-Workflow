import json, subprocess, sys, pathlib

def test_smoke_run():
    repo = pathlib.Path(__file__).resolve().parents[1]
    wf = repo / "workflows" / "workflow.json"
    cmd = [sys.executable, str(repo / "langgraph_builder.py"), "--workflow", str(wf), "--run"]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stderr
    assert "FINAL OUTPUT" in proc.stdout
