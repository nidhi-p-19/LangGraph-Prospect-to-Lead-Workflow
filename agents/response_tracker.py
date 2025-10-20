from __future__ import annotations
from typing import Dict, Any
from agents.base import BaseAgent
from tools.clients import mock_responses

class ResponseTrackerAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        campaign_id = payload.get("campaign_id","cmp-mock-001")
        self._log("input", {"campaign": campaign_id})
        responses = mock_responses(payload.get("sent_status", []))
        self._log("output", {"count": len(responses)})
        return {"responses": responses}
