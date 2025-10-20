from __future__ import annotations
from typing import Dict, Any, List
from agents.base import BaseAgent
from tools.clients import GoogleSheetsClient, mock_recos

def compute_metrics(responses: List[Dict[str, Any]]) -> Dict[str, float]:
    n = len(responses) or 1
    opens = sum(r.get("opened", False) for r in responses)
    clicks = sum(r.get("clicked", False) for r in responses)
    replies = sum(r.get("replied", False) for r in responses)
    meetings = sum(r.get("booked_meeting", False) for r in responses)
    return {
        "open_rate": opens / n,
        "click_rate": clicks / n,
        "reply_rate": replies / n,
        "meeting_rate": meetings / n,
    }

class FeedbackTrainerAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        responses = payload.get("responses", [])
        self._log("input", {"count": len(responses)})
        metrics = compute_metrics(responses)
        recos = mock_recos(metrics)
        self._log("metrics", metrics)
        self._log("recommendations", recos)

        gs = GoogleSheetsClient()
        rows = [["timestamp","metric","value"]] + [[self.id, k, f"{v:.3f}"] for k,v in metrics.items()]
        gs.append_recommendations(rows)

        return {"recommendations": recos, "metrics": metrics}
