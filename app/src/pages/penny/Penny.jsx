import { useEffect, useState, useRef } from "react";
import styles from "./Penny.module.css";
import { WEBSOCKET_URL } from "../../env";

const USER_ID = "a9c0963f-337c-5884-885c-8c8f8f8d3d82";

const AGENT_COLORS = {
  orchestrator: "#818cf8",
  agent_api: "#34d399",
};

function agentColor(agent) {
  return AGENT_COLORS[agent] || "#94a3b8";
}

export default function Penny() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [wsStatus, setWsStatus] = useState("connecting");

  const wsRef = useRef(null);
  const reconnectTimer = useRef(null);
  const currentAssistantMessage = useRef("");
  const currentThinking = useRef({});
  const currentAgents = useRef(new Set());
  const containerRef = useRef(null);

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
          setMessages((prev) => [
            ...prev,
            { role: "assistant", text: "", thinking: {}, agents: [], isStreaming: true },
          ]);
        } else if (msg.type === "thinking_chunk") {
          const chunk = msg.data || "";
          const agent = msg.agent || "unknown";
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
          const agent = msg.agent || "unknown";
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
        <div className={styles.statusBadge}>
          <span className={`${styles.dot} ${statusDot}`} />
          <span className={styles.statusText}>{wsStatus}</span>
        </div>
      </div>

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
                    {m.text || <span className={styles.typingDots}><span /><span /><span /></span>}
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
                            <span className={styles.thinkingAgent}>{agent}</span>
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
                          ● {a}
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
  );
}
