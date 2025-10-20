from __future__ import annotations
from typing import Dict, Any
from agents.base import BaseAgent
from tools.clients import mock_enrich

class DataEnrichmentAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        leads = payload.get("leads", [])
        self._log("input", {"count": len(leads)})
        enriched = mock_enrich(leads)
        self._log("output", {"count": len(enriched)})
        return {"enriched_leads": enriched}
