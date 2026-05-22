import asyncio
from fastapi import WebSocket

from shared.logger import Logger

logger = Logger(__name__)


class AgentCallbackHandler:
    """
    Shared callback handler created once per WebSocket turn.

    Owns the socket, the running event loop, and the rolling state
    (full_response, reasoning_text, tools_used, events) for ALL agents in
    the turn. Per-agent identity and silence are injected by
    SilentCallbackHandler before each call reaches __call__.

    Gating rules:
      - data (response tokens)   : sent only if silent=False
      - reasoningText            : sent only if silent=False
      - tool_use_started         : ALWAYS sent (UI must show progress)
      - tool_result              : ALWAYS sent
    Every event is appended to self.events with internal=silent and agent_id
    for tracing / replay.
    """

    def __init__(self, websocket: WebSocket, loop: asyncio.AbstractEventLoop):
        self.websocket = websocket
        self.loop = loop

        self.full_response = ""
        self.reasoning_text = ""
        self.tools_used: dict = {}
        self.events: list = []
        self.is_connection_available = True

    def __call__(self, *, agent_id: str, silent: bool, **kwargs):
        try:
            self._handle_reasoning(agent_id, silent, kwargs)
            self._handle_response_token(agent_id, silent, kwargs)
            self._handle_tool_use_started(agent_id, silent, kwargs)
            self._handle_tool_in_progress(agent_id, kwargs)
            self._handle_tool_result(agent_id, silent, kwargs)
        except Exception as e:
            logger.error(f"Callback handler error for agent {agent_id}: {e}")

    def _handle_reasoning(self, agent_id: str, silent: bool, kwargs: dict):
        chunk = kwargs.get("reasoningText")
        if not chunk:
            return
        self.reasoning_text += chunk
        self.events.append({
            "type": "reasoning",
            "agent_id": agent_id,
            "internal": silent,
            "data": chunk,
        })
        if not silent:
            self._send({"type": "thinking_chunk", "agent_id": agent_id, "data": chunk})

    def _handle_response_token(self, agent_id: str, silent: bool, kwargs: dict):
        if "data" not in kwargs:
            return
        chunk = kwargs["data"]
        self.full_response += chunk
        self.events.append({
            "type": "response",
            "agent_id": agent_id,
            "internal": silent,
            "data": chunk,
        })
        if not silent:
            self._send({"type": "chunk", "agent_id": agent_id, "data": chunk})

    def _handle_tool_use_started(self, agent_id: str, silent: bool, kwargs: dict):
        event = kwargs.get("event") or {}
        tool_use = (
            event.get("contentBlockStart", {})
            .get("start", {})
            .get("toolUse")
        )
        if not tool_use:
            return
        tool_id = tool_use.get("toolUseId")
        tool_name = tool_use.get("name")
        if not tool_id:
            return
        self.tools_used[tool_id] = {
            "name": tool_name,
            "agent_id": agent_id,
            "status": "started",
            "input": None,
            "result": None,
        }
        self.events.append({
            "type": "tool_call",
            "agent_id": agent_id,
            "internal": silent,
            "tool": tool_name,
            "tool_id": tool_id,
        })
        # Tool progress is ALWAYS surfaced, even from silent agents.
        self._send({
            "type": "tool_use_started",
            "agent_id": agent_id,
            "tool": tool_name,
            "tool_id": tool_id,
        })

    def _handle_tool_in_progress(self, agent_id: str, kwargs: dict):
        current = kwargs.get("current_tool_use")
        if not current:
            return
        tool_id = current.get("toolUseId") or current.get("tool_use_id")
        if not tool_id or tool_id not in self.tools_used:
            return
        self.tools_used[tool_id]["status"] = "in_progress"
        self.tools_used[tool_id]["input"] = current.get("input")

    def _handle_tool_result(self, agent_id: str, silent: bool, kwargs: dict):
        message = kwargs.get("message")
        if not message or message.get("role") != "user":
            return
        for block in message.get("content", []) or []:
            tool_result = block.get("toolResult") if isinstance(block, dict) else None
            if not tool_result:
                continue
            tool_id = tool_result.get("toolUseId")
            content_blocks = tool_result.get("content", []) or []
            text_parts = [
                b.get("text", "") for b in content_blocks if isinstance(b, dict)
            ]
            result_text = "".join(text_parts)
            tool_name = None
            if tool_id and tool_id in self.tools_used:
                self.tools_used[tool_id]["status"] = "completed"
                self.tools_used[tool_id]["result"] = result_text
                tool_name = self.tools_used[tool_id].get("name")
            self.events.append({
                "type": "tool_result",
                "agent_id": agent_id,
                "internal": silent,
                "tool": tool_name,
                "tool_id": tool_id,
                "data": result_text,
            })
            self._send({
                "type": "tool_result",
                "agent_id": agent_id,
                "tool": tool_name,
                "tool_id": tool_id,
                "data": result_text,
            })

    def _send(self, payload: dict):
        if not self.is_connection_available:
            return
        asyncio.run_coroutine_threadsafe(self._send_async(payload), self.loop)

    async def _send_async(self, payload: dict):
        try:
            await self.websocket.send_json(payload)
        except Exception as e:
            self.is_connection_available = False
            logger.warning(f"WebSocket send failed, marking connection unavailable: {e}")


class SilentCallbackHandler:
    """
    Per-agent wrapper. Stamps agent_id and silent onto every callback before
    delegating to the shared AgentCallbackHandler.

    Not a no-op: it always forwards the event; it just attaches the agent's
    identity and silence preference so the shared handler can decide what
    to surface to the user.
    """

    def __init__(self, callback: AgentCallbackHandler, agent_id: str, silent: bool = True):
        self.callback = callback
        self.agent_id = agent_id
        self.silent = silent

    def __call__(self, **kwargs):
        self.callback(agent_id=self.agent_id, silent=self.silent, **kwargs)