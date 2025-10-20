from __future__ import annotations
from typing import Dict, Any, List

from agents.base import BaseAgent

def score_lead(lead: Dict[str, Any], criteria: Dict[str, Any]) -> float:
    score = 0.0
    if "VP" in lead.get("role",""):
        score += 0.3
    tech = set(lead.get("technologies", []))
    prefer = set(criteria.get("preferred_tech", []))
    avoid = set(criteria.get("avoid_tech", []))
    score += 0.2 * (len(tech & prefer))
    score -= 0.2 * (len(tech & avoid))
    signal = lead.get("signal","")
    if signal in ("recent_funding","hiring_for_sales"):
        score += 0.3
    return max(0.0, min(1.0, score))

class ScoringAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        leads = payload.get("enriched_leads", [])
        criteria = payload.get("scoring_criteria", {})
        ranked: List[Dict[str, Any]] = []
        for L in leads:
            s = score_lead(L, criteria)
            ranked.append({"lead": L, "score": round(s, 3)})
        ranked.sort(key=lambda x: x["score"], reverse=True)
        self._log("output", {"top": ranked[:3]})
        return {"ranked_leads": ranked}
