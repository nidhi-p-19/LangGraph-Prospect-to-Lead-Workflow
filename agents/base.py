from __future__ import annotations
from typing import Any, Dict
from utils.logger import log_event

class BaseAgent:
    id: str = "base"

    def __init__(self, node_id: str, instructions: str | None = None, tools: list[dict] | None = None):
        self.id = node_id
        self.instructions = instructions or ""
        self.tools = tools or []

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

    def _log(self, kind: str, payload):
        log_event(self.id, kind, payload)
