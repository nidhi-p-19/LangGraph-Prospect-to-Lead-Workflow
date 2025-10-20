from __future__ import annotations
import json, pathlib, datetime as dt

RUN_DIR = pathlib.Path(".runs")
RUN_DIR.mkdir(exist_ok=True)

def ts() -> str:
    return dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def log_event(node_id: str, kind: str, payload):
    rec = {"ts": ts(), "node": node_id, "kind": kind, "payload": payload}
    path = RUN_DIR / f"{node_id}.log"
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
