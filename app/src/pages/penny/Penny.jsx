import { useEffect, useState, useRef } from "react";
import ReactMarkdown from "react-markdown";
import styles from "./Penny.module.css";
import { WEBSOCKET_URL } from "../../env";

const USER_ID = "a9c0963f-337c-5884-885c-8c8f8f8d3d82";

const AGENT_COLORS = {
  orchestrator_agent: "#818cf8",
  analyst_agent: "#34d399",
  artifact_agent: "#f59e0b",
};

function agentColor(agent) {
  return AGENT_COLORS[agent] || "#94a3b8";
}

function agentLabel(agent) {
  if (!agent) return "unknown";
  return agent.replace(/_agent$/, "");
}

export default function Penny() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [wsStatus, setWsStatus] = useState("connecting");
  const [debugMode, setDebugMode] = useState(false);
  const [debugTurns, setDebugTurns] = useState([]); // [{ id, startedAt, eventsByAgent: { agent_id: [event] } }]
  const [debugPanelWidth, setDebugPanelWidth] = useState(360);

  const wsRef = useRef(null);
  const reconnectTimer = useRef(null);
  const currentAssistantMessage = useRef("");
  const currentThinking = useRef({});
  const currentAgents = useRef(new Set());
  const currentTurnId = useRef(null);
  const containerRef = useRef(null);
  const resizingRef = useRef(false);
  const resizeStartX = useRef(0);
  const resizeStartWidth = useRef(0);

  const onResizeMouseDown = (e) => {
    e.preventDefault();
    resizingRef.current = true;
    resizeStartX.current = e.clientX;
    resizeStartWidth.current = debugPanelWidth;
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";

    const onMouseMove = (ev) => {
      if (!resizingRef.current) return;
      // dragging left (toward chat) increases panel width
      const delta = resizeStartX.current - ev.clientX;
      const next = Math.max(220, Math.min(640, resizeStartWidth.current + delta));
      setDebugPanelWidth(next);
    };

    const onMouseUp = () => {
      resizingRef.current = false;
      document.body.style.cursor = "";
      document.body.style.userSelect = "";
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
    };

    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
  };

  const pushDebugEvent = (msg) => {
    const turnId = currentTurnId.current;
    if (!turnId) return;
    const agentId = msg.agent_id || "system";
    setDebugTurns((prev) => {
      const updated = [...prev];
      const idx = updated.findIndex((t) => t.id === turnId);
      if (idx === -1) return prev;
      const turn = { ...updated[idx] };
      const groups = { ...turn.eventsByAgent };
      const list = groups[agentId] ? [...groups[agentId]] : [];
      list.push({ ...msg, ts: Date.now() });
      groups[agentId] = list;
      turn.eventsByAgent = groups;
      updated[idx] = turn;
      return updated;
    });
  };

  const connectWebSocket = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(`${WEBSOCKET_URL}penny/v1/ws/${USER_ID}/chat`);
    wsRef.current = ws;

    ws.onopen = () => {
      setWsStatus("connected");
      console.log("WS connected");
    };

    ws.onerror = (e) => {
      setWsStatus("error");
      console.error("WS error:", e);
    };

    ws.onclose = () => {
      setWsStatus("reconnecting");
      console.warn("WS closed. Reconnecting...");
      reconnectTimer.current = setTimeout(connectWebSocket, 2000);
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);

        if (msg.type === "response_start") {
          currentAssistantMessage.current = "";
          currentThinking.current = {};
          currentAgents.current = new Set();
          const turnId = `turn-${Date.now()}`;
          currentTurnId.current = turnId;
          setDebugTurns((prev) => [
            ...prev,
            { id: turnId, startedAt: Date.now(), eventsByAgent: {} },
          ]);
          setMessages((prev) => [
            ...prev,
            { role: "assistant", text: "", thinking: {}, agents: [], isStreaming: true },
          ]);
        } else if (msg.type === "thinking_chunk") {
          const chunk = msg.data || "";
          const agent = msg.agent_id || msg.agent || "unknown";
          currentThinking.current = {
            ...currentThinking.current,
            [agent]: (currentThinking.current[agent] || "") + chunk,
          };

          setMessages((prev) => {
            const updated = [...prev];
            const last = { ...updated[updated.length - 1] };
            last.thinking = { ...currentThinking.current };
            updated[updated.length - 1] = last;
            return updated;
          });
        } else if (msg.type === "chunk") {
          const chunk = msg.data || "";
          const agent = msg.agent_id || msg.agent || "unknown";
          currentAssistantMessage.current += chunk;
          currentAgents.current.add(agent);

          setMessages((prev) => {
            const updated = [...prev];
            const last = { ...updated[updated.length - 1] };
            last.text = currentAssistantMessage.current;
            last.agents = Array.from(currentAgents.current);
            updated[updated.length - 1] = last;
            return updated;
          });
        } else if (msg.type === "tool_use_started" || msg.type === "tool_result") {
          pushDebugEvent(msg);
        } else if (msg.type === "response_end") {
          setMessages((prev) => {
            const updated = [...prev];
            const last = { ...updated[updated.length - 1] };
            last.isStreaming = false;
            updated[updated.length - 1] = last;
            return updated;
          });
        } else if (msg.type === "response_error") {
          setMessages((prev) => [
            ...prev,
            { role: "error", text: msg.data || "An error occurred." },
          ]);
          pushDebugEvent(msg);
        }
      } catch {
        console.log("Non-JSON:", event.data);
      }
    };
  };

  useEffect(() => {
    connectWebSocket();
    return () => {
      clearTimeout(reconnectTimer.current);
      wsRef.current?.close();
    };
  }, []);

  useEffect(() => {
    if (containerRef.current)
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
  }, [messages]);

  const sendMessage = () => {
    if (!input.trim()) return;
    if (wsRef.current?.readyState !== WebSocket.OPEN) return;

    setMessages((prev) => [...prev, { role: "user", text: input }]);
    wsRef.current.send(input);
    setInput("");
  };

  const clearDebug = () => setDebugTurns([]);

  const statusDot = {
    connected: styles.dotGreen,
    connecting: styles.dotYellow,
    reconnecting: styles.dotYellow,
    error: styles.dotRed,
  }[wsStatus] || styles.dotYellow;

  return (
    <div className={styles.wrapper}>
      {/* HEADER */}
      <div className={styles.header}>
        <div className={styles.headerLeft}>
          <span className={styles.headerTitle}>Penny</span>
          <span className={styles.headerSub}>AI Financial Assistant</span>
        </div>
        <div className={styles.headerRight}>
          <button
            type="button"
            className={`${styles.debugToggle} ${debugMode ? styles.debugToggleOn : ""}`}
            onClick={() => setDebugMode((v) => !v)}
            aria-pressed={debugMode}
            title="Toggle debug panel"
          >
            <span className={`${styles.dot} ${debugMode ? styles.dotPurple : styles.dotGray}`} />
            <span className={styles.debugToggleText}>debug {debugMode ? "on" : "off"}</span>
          </button>
          <div className={styles.statusBadge}>
            <span className={`${styles.dot} ${statusDot}`} />
            <span className={styles.statusText}>{wsStatus}</span>
          </div>
        </div>
      </div>

      <div className={styles.body}>
        {/* CHAT COLUMN */}
        <div className={styles.chatColumn}>
          {/* CHAT AREA */}
          <div ref={containerRef} className={styles.chatArea}>
            {messages.length === 0 ? (
              <div className={styles.placeholder}>
                <div className={styles.placeholderIcon}>✦</div>
                <p>Ask Penny anything about your finances</p>
              </div>
            ) : (
              messages.map((m, i) => {
                if (m.role === "user") {
                  return (
                    <div key={i} className={`${styles.messageRow} ${styles.right}`}>
                      <div className={`${styles.bubble} ${styles.userBubble}`}>
                        {m.text}
                      </div>
                    </div>
                  );
                }
                if (m.role === "error") {
                  return (
                    <div key={i} className={`${styles.messageRow} ${styles.left}`}>
                      <div className={`${styles.bubble} ${styles.errorBubble}`}>
                        <span className={styles.errorIcon}>⚠</span> {m.text}
                      </div>
                    </div>
                  );
                }
                // assistant
                return (
                  <div key={i} className={`${styles.messageRow} ${styles.left}`}>
                    <div className={styles.assistantGroup}>
                      <div className={`${styles.bubble} ${styles.assistantBubble} ${m.isStreaming ? styles.streaming : ""}`}>
                        {m.text
                            ? <ReactMarkdown>{m.text}</ReactMarkdown>
                            : <span className={styles.typingDots}><span /><span /><span /></span>}
                      </div>
                      {m.thinking && Object.keys(m.thinking).length > 0 && (
                        <div className={styles.thinkingGroup}>
                          {Object.entries(m.thinking).map(([agent, text]) => (
                            <details key={agent} className={styles.thinkingDetails}>
                              <summary
                                className={styles.thinkingSummary}
                                style={{ "--thinking-color": agentColor(agent) }}
                              >
                                <span className={styles.thinkingIcon}>⚙</span>
                                <span className={styles.thinkingAgent}>{agentLabel(agent)}</span>
                                <span className={styles.thinkingLabel}>thinking</span>
                              </summary>
                              <pre className={styles.thinkingContent}>{text}</pre>
                            </details>
                          ))}
                        </div>
                      )}
                      {m.agents && m.agents.length > 0 && (
                        <div className={styles.agentPills}>
                          {m.agents.map((a) => (
                            <span
                              key={a}
                              className={styles.agentPill}
                              style={{ "--pill-color": agentColor(a) }}
                            >
                              ● {agentLabel(a)}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                );
              })
            )}
          </div>

          {/* INPUT BAR */}
          <div className={styles.inputArea}>
            <input
              type="text"
              className={styles.input}
              placeholder="Message Penny..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              disabled={wsStatus !== "connected"}
            />
            <button
              className={styles.sendBtn}
              onClick={sendMessage}
              disabled={!input.trim() || wsStatus !== "connected"}
              aria-label="Send"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13" />
                <polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            </button>
          </div>
        </div>

        {/* DEBUG PANEL */}
        {debugMode && (
          <aside className={styles.debugPanel} style={{ width: debugPanelWidth }}>
            <div className={styles.debugResizeHandle} onMouseDown={onResizeMouseDown} title="Drag to resize" />
            <div className={styles.debugHeader}>
              <span className={styles.debugTitle}>Agent Debug</span>
              <button type="button" className={styles.debugClear} onClick={clearDebug}>
                clear
              </button>
            </div>
            <div className={styles.debugBody}>
              {debugTurns.length === 0 ? (
                <div className={styles.debugEmpty}>No events yet. Send a message to see agent activity.</div>
              ) : (
                debugTurns.map((turn, ti) => (
                  <div key={turn.id} className={styles.debugTurn}>
                    <div className={styles.debugTurnHeader}>
                      Turn #{ti + 1} · {new Date(turn.startedAt).toLocaleTimeString()}
                    </div>
                    {Object.entries(turn.eventsByAgent).map(([agentId, events]) => (
                      <details key={agentId} className={styles.debugAgentGroup} open>
                        <summary
                          className={styles.debugAgentSummary}
                          style={{ "--agent-color": agentColor(agentId) }}
                        >
                          <span className={`${styles.dot} ${styles.dotInline}`} style={{ background: agentColor(agentId) }} />
                          <span className={styles.debugAgentName}>{agentLabel(agentId)}</span>
                          <span className={styles.debugEventCount}>{events.length}</span>
                        </summary>
                        <div className={styles.debugEventList}>
                          {events.map((ev, ei) => (
                            <DebugEvent key={ei} ev={ev} />
                          ))}
                        </div>
                      </details>
                    ))}
                  </div>
                ))
              )}
            </div>
          </aside>
        )}
      </div>
    </div>
  );
}

function DebugEvent({ ev }) {
  const time = new Date(ev.ts).toLocaleTimeString();
  let body = null;

  if (ev.type === "tool_use_started") {
    body = (
      <>
        <span className={styles.debugEventTag} data-kind="tool-start">tool ▶</span>
        <span className={styles.debugEventName}>{ev.tool}</span>
      </>
    );
  } else if (ev.type === "tool_result") {
    body = (
      <>
        <span className={styles.debugEventTag} data-kind="tool-end">tool ✓</span>
        <span className={styles.debugEventName}>{ev.tool}</span>
      </>
    );

  } else if (ev.type === "response_error") {
    body = (
      <>
        <span className={styles.debugEventTag} data-kind="error">error</span>
        <span className={styles.debugEventName}>{ev.data}</span>
      </>
    );
  } else {
    body = <span className={styles.debugEventName}>{ev.type}</span>;
  }

  const hasDetail = ev.type === "tool_result" || ev.type === "tool_use_started";

  return (
    <details className={styles.debugEvent}>
      <summary className={styles.debugEventSummary}>
        <span className={styles.debugEventTime}>{time}</span>
        {body}
      </summary>
      {hasDetail && (
        <pre className={styles.debugEventDetail}>
{JSON.stringify(
  {
    tool: ev.tool,
    tool_id: ev.tool_id,
    data: ev.data,
  },
  null,
  2
)}
        </pre>
      )}
    </details>
  );
}

