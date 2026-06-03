# Stop Button Plan

## Research Summary: LM Studio Stop Signal

### What the Docs Say
LM Studio exposes **no explicit "cancel inference" endpoint** on either its native REST API (`/api/v1/chat`) or its OpenAI-compatible endpoint (`/v1/chat/completions`).

The only documented way to stop generation is to **close / abort the HTTP request**. When LM Studio detects the client has dropped the connection it stops generating tokens.

We are currently using:
- **Strands `OpenAIModel`** → wraps the **OpenAI Python SDK** → which uses **`httpx`** under the hood
- The agent runs in a `ThreadPoolExecutor` thread (one thread per turn)

Since Strands does not expose a native "cancel" hook, the correct approach is a **stop flag checked inside the callback handler**. When the flag fires we raise an exception, which propagates out of the Strands agent loop and terminates the executor thread — which also drops the in-flight `httpx` connection to LM Studio, stopping generation server-side.

---

## Architecture: How Stop Will Work

```
UI ──(WebSocket "stop" message)──► Backend WebSocket handler
                                        │
                                        ▼
                              threading.Event (stop_event)
                                        │
                                        ▼
                          AgentCallbackHandler.__call__
                          checks stop_event on every token
                                        │
                                        ▼
                          raises StopIteration → Strands exits
                          → executor thread ends
                          → httpx connection dropped
                          → LM Studio stops generating
```

---

## Changes Required

### 1. `AgentCallbackHandler` — add stop flag (`callback_handler.py`)

- Add a `threading.Event` called `stop_event` to the handler.
- Expose a `stop()` method that sets the event.
- At the top of `__call__`, check `self.stop_event.is_set()` and raise `StopIteration` to abort the agent.
- Send a `{"type": "response_stopped"}` event to the UI before raising so the UI knows to finalise the message.

```python
import threading

class AgentCallbackHandler:
    def __init__(self, websocket, loop):
        ...
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def __call__(self, *, agent_id, silent, **kwargs):
        if self.stop_event.is_set():
            self._send({"type": "response_stopped", "data": ""})
            raise StopIteration("Agent stopped by user")
        ...  # existing logic unchanged
```

### 2. `AgentUseCase` — listen for stop message concurrently (`agent.py`)

The current flow `await loop.run_in_executor(executor, run_agent)` blocks the coroutine — it cannot receive a WebSocket message while waiting. Fix: run the executor as an `asyncio.Task` and concurrently `await websocket.receive_text()` for a stop signal.

```python
async def execute(self, query: str, shared_callback: AgentCallbackHandler):
    agent_task = asyncio.get_event_loop().run_in_executor(executor, run_agent)
    agent_future = asyncio.ensure_future(agent_task)

    while not agent_future.done():
        try:
            raw = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
            msg = json.loads(raw)
            if msg.get("type") == "stop":
                shared_callback.stop()
                break
        except asyncio.TimeoutError:
            continue  # no message yet, keep waiting

    await agent_future  # collect result / exception
```

> **Note:** `StopIteration` raised inside a thread does not cross the thread boundary cleanly in Python — use a custom exception class (e.g. `AgentStoppedError`) instead.

### 3. WebSocket endpoint — forward `shared_callback` to `execute` (`endpoints/agent.py`)

`AgentUseCase` currently creates `shared_callback` internally. Refactor so it is created once per turn and passed in, or just keep it internal but expose `execute` to receive the stop via the loop above.

The simplest change: `AgentUseCase.execute()` now accepts an optional `stop_event` and creates the callback with it. The WebSocket loop passes a `stop_event` it watches.

### 4. UI — swap Send ↔ Stop button (`Penny.jsx`)

- Add `isStreaming` state (already present on message objects; add a top-level `useState`).
- When `response_start` arrives → set `isStreaming = true`.
- When `response_end` or `response_stopped` arrives → set `isStreaming = false`.
- Render the send button conditionally:

```jsx
{isStreaming ? (
  <button className={styles.stopBtn} onClick={stopStreaming} aria-label="Stop">
    {/* square stop icon */}
    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
      <rect x="3" y="3" width="10" height="10" rx="2" />
    </svg>
  </button>
) : (
  <button className={styles.sendBtn} onClick={sendMessage}
          disabled={!input.trim() || wsStatus !== "connected"} aria-label="Send">
    {/* existing arrow SVG */}
  </button>
)}
```

- `stopStreaming` sends the stop message and marks the last message as no longer streaming:

```js
const stopStreaming = () => {
  if (wsRef.current?.readyState === WebSocket.OPEN) {
    wsRef.current.send(JSON.stringify({ type: "stop" }));
  }
};
```

---

## Message Protocol Addition

| Direction | Message | Meaning |
|-----------|---------|---------|
| UI → Backend | `{"type": "stop"}` | User clicked Stop |
| Backend → UI | `{"type": "response_stopped", "data": ""}` | Agent has been interrupted; treat like `response_end` |

---

## Implementation Order

1. `callback_handler.py` — add `stop_event`, `stop()` method, check at top of `__call__`, raise custom `AgentStoppedError`, send `response_stopped`.
2. `agent.py` (use case) — concurrent receive loop, call `shared_callback.stop()` on stop message, catch `AgentStoppedError` gracefully.
3. `endpoints/agent.py` — the outer `while True` loop already reads messages; refactor so it can distinguish user messages from stop signals and route them to the correct handler.
4. `Penny.jsx` — add top-level `isStreaming` state, handle `response_stopped` as equivalent to `response_end`, swap buttons.
5. `Penny.module.css` — add `.stopBtn` style (red/danger colour, same shape as `.sendBtn`).

---

## LM Studio API — Current vs Ideal

| | Current (OpenAI-compat) | Native `/api/v1/chat` |
|---|---|---|
| Stop signal | Drop HTTP connection (happens automatically when executor thread raises) | Same — no explicit cancel endpoint |
| Streaming | SSE via OpenAI SDK | SSE with richer events (`chat.start`, `message.delta`, `chat.end`, etc.) |
| Stateful chat | ❌ (full history sent each time) | ✅ (`previous_response_id`) |
| Custom tools | ✅ (what Strands uses) | ❌ |
| Reasoning events | Partial (reasoning tokens via Strands callback) | `reasoning.start / .delta / .end` events |

**Conclusion**: stay on the **OpenAI-compatible** endpoint because Strands requires it for custom tool support. The stop mechanism (drop connection via exception) works identically on both endpoints.
