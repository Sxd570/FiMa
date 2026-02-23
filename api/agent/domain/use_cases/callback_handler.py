from fastapi import WebSocket, WebSocketDisconnect
from shared.logger import Logger
import asyncio

logger = Logger(__name__)

class WebSocketCallback:
    def __init__(self, websocket: WebSocket, agent_name: str):
        self.websocket = websocket
        self.agent_name = agent_name
        self.response = ""
        self._loop = asyncio.get_running_loop()

    def __call__(self, **kwargs):
        if "data" in kwargs:
            chunk = kwargs["data"]
            self.response += chunk
            asyncio.run_coroutine_threadsafe(
                self._send_chunk_async(chunk),
                self._loop
            )

    async def _send_chunk_async(self, chunk: str):
        try:
            await self.websocket.send_json({
                "type": "chunk",
                "agent": self.agent_name,
                "data": chunk
            })
        except Exception as e:
            logger.error(f"Error sending chunk from {self.agent_name}: {e}")

    def clear(self):
        self.response = ""