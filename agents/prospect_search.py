from __future__ import annotations
from typing import Dict, Any, List
from agents.base import BaseAgent
from tools.clients import ApolloClient, ClayClient

class ProspectSearchAgent(BaseAgent):
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        icp = payload.get("icp", {})
        signals = payload.get("signals", [])
        limit = int(payload.get("_limit", 20))

        self._log("input", {"icp": icp, "signals": signals, "limit": limit})

        apollo = ApolloClient()
        clay = ClayClient()

        A = apollo.search({"icp": icp, "signals": signals})
        C = clay.search({"icp": icp, "signals": signals})
        combined = {(l["company"], l["email"]): l for l in (A + C)}
        leads = list(combined.values())[:limit]

        self._log("output", {"count": len(leads)})
        return {"leads": leads}
