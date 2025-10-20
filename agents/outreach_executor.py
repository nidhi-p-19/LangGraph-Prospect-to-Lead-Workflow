from __future__ import annotations
from typing import Dict, Any
from agents.base import BaseAgent
from tools.clients import mock_send

class OutreachExecutorAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        messages = payload.get("messages", [])
        self._log("input", {"count": len(messages)})
        results = mock_send(messages)
        self._log("output", {"count": len(results)})
        return {"sent_status": results, "campaign_id": "cmp-mock-001"}
