from __future__ import annotations
import argparse, json, re, sys, pathlib
from typing import Any, Dict
from dotenv import load_dotenv
from utils.logger import log_event

AGENT_MAP = {
    "ProspectSearchAgent": "agents.prospect_search:ProspectSearchAgent",
    "DataEnrichmentAgent": "agents.enrichment:DataEnrichmentAgent",
    "ScoringAgent": "agents.scoring:ScoringAgent",
    "OutreachContentAgent": "agents.outreach_content:OutreachContentAgent",
    "OutreachExecutorAgent": "agents.outreach_executor:OutreachExecutorAgent",
    "ResponseTrackerAgent": "agents.response_tracker:ResponseTrackerAgent",
    "FeedbackTrainerAgent": "agents.feedback_trainer:FeedbackTrainerAgent",
}

def dimport(path: str):
    mod, cls = path.split(":")
    m = __import__(mod, fromlist=[cls])
    return getattr(m, cls)

def render_refs(obj: Any, ctx: Dict[str, Any]) -> Any:
    import re, json

    # If the whole value is exactly a single {{ref}}, return the real object
    if isinstance(obj, str):
        m = re.fullmatch(r"\{\{([^}]+)\}\}", obj)
        if m:
            path = m.group(1).strip()
            cur = ctx
            for p in path.split("."):
                if p not in cur:
                    return obj  # leave unresolved if missing
                cur = cur[p]
            return cur  # <-- return the actual object (list/dict/str/num)

        # Otherwise, allow inline string substitutions inside a larger string
        def repl(mm):
            path = mm.group(1).strip()
            cur = ctx
            for p in path.split("."):
                if p not in cur:
                    return mm.group(0)  # leave unresolved
                cur = cur[p]
            # When embedding inside a string, convert to string
            return cur if isinstance(cur, str) else json.dumps(cur)

        return re.sub(r"\{\{([^}]+)\}\}", repl, obj)

    if isinstance(obj, list):
        return [render_refs(x, ctx) for x in obj]
    if isinstance(obj, dict):
        return {k: render_refs(v, ctx) for k, v in obj.items()}
    return obj


def run_workflow(workflow: Dict[str, Any]) -> Dict[str, Any]:
    steps = workflow.get("steps", [])
    ctx: Dict[str, Any] = {"config": workflow.get("config", {}), "steps": {}}
    prev_output = None
    for step in steps:
        node_id = step["id"]
        agent_name = step["agent"]
        inputs = step.get("inputs", {})
        instructions = step.get("instructions", "")
        tools = step.get("tools", [])

        rich_ctx = {**ctx, node_id: {"output": prev_output}, **{s["id"]: {"output": ctx["steps"].get(s["id"], {})} for s in steps}}
        inputs = render_refs(inputs, rich_ctx)

        AgentCls = dimport(AGENT_MAP[agent_name])
        agent = AgentCls(node_id=node_id, instructions=instructions, tools=tools)
        log_event(node_id, "start", {"inputs": inputs})
        out = agent.run(inputs)
        ctx["steps"][node_id] = out
        prev_output = out
        log_event(node_id, "end", {"output_keys": list(out.keys())})
    return ctx

def main():
    load_dotenv()
    ap = argparse.ArgumentParser()
    ap.add_argument("--workflow", required=True)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    wf_path = pathlib.Path(args.workflow)
    if not wf_path.exists():
        print(f"Workflow not found: {wf_path}", file=sys.stderr); sys.exit(2)

    workflow = json.loads(wf_path.read_text(encoding="utf-8"))
    print(f"Loaded workflow: {workflow.get('workflow_name')}")

    if args.dry_run and args.run:
        print("--dry-run and --run are mutually exclusive", file=sys.stderr); sys.exit(2)

    if args.dry_run:
        print("Validation OK."); return

    ctx = run_workflow(workflow)
    last_id = workflow["steps"][-1]["id"]
    final = ctx["steps"][last_id]
    print("\n=== FINAL OUTPUT ===")
    print(json.dumps(final, indent=2))

if __name__ == "__main__":
    main()

