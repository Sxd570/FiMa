import { useEffect, useState, useRef } from "react";
import styles from "./Penny.module.css";

export default function Penny() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Mock conversations list — you can replace with API
  const [conversations, setConversations] = useState([
    { id: 1, title: "Conversation 1" },
    { id: 2, title: "Design Discussion" },
    { id: 3, title: "Project Plan" },
  ]);

  const wsRef = useRef(null);
  const reconnectTimer = useRef(null);
  const currentAssistantMessage = useRef("");

  // Connect WebSocket
  const connectWebSocket = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket("ws://localhost:8001/penny/v1/ws/123/chat");
    wsRef.current = ws;

    ws.onopen = () => console.log("WS connected");
    ws.onerror = (e) => console.error("WS error:", e);

    ws.onclose = () => {
      console.warn("WS closed. Reconnecting...");
      reconnectTimer.current = setTimeout(connectWebSocket, 2000);
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);

        if (msg.type === "response_start") {
          currentAssistantMessage.current = "";
          setMessages((prev) => [
            ...prev,
            { role: "assistant", text: "", isStreaming: true },
          ]);
        } else if (msg.type === "chunk") {
          const chunk = msg.data || "";
          currentAssistantMessage.current += chunk;

          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            last.text = currentAssistantMessage.current;
            return updated;
          });
        } else if (msg.type === "response_end") {
          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            last.isStreaming = false;
            return updated;
          });
        }
      } catch {
        console.log("Non-JSON:", event.data);
      }
    };
  };

  // useEffect(() => {
  //   connectWebSocket();
  //   return () => clearTimeout(reconnectTimer.current);
  // }, []);

  const sendMessage = () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: "user", text: input }]);

    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(input);
    }

    setInput("");
  };

  const ChatBubble = ({ role, text }) => {
    const isUser = role === "user";
    return (
      <div
        className={`${styles.messageRow} ${isUser ? styles.right : styles.left}`}
      >
        <div
          className={`${styles.bubble} ${
            isUser ? styles.userBubble : styles.assistantBubble
          }`}
        >
          {text}
        </div>
      </div>
    );
  };

  const containerRef = useRef(null);
  useEffect(() => {
    if (containerRef.current)
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
  }, [messages]);

  return (
    <div className={styles.wrapper}>
      {/* SIDEBAR */}
      <div
        className={`${styles.sidebar} ${
          sidebarOpen ? styles.sidebarOpen : styles.sidebarClosed
        }`}
      >
        <div className={styles.sidebarHeader}>
          <span>Conversations</span>
          <div className={styles.toggleWrapper}>
  
</div>
        </div>

        {sidebarOpen && (
          <div className={styles.convoList}>
            {conversations.map((c) => (
              <div key={c.id} className={styles.convoItem}>
                {c.title}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* MAIN CHAT AREA */}
      <div className={styles.container}>
        <div ref={containerRef} className={styles.chatArea}>
          {messages.length === 0 ? (
            <div className={styles.placeholder}>Start chatting with your agent...</div>
          ) : (
            messages.map((m, i) => (
              <ChatBubble key={i} role={m.role} text={m.text} />
            ))
          )}
        </div>

        <div className={styles.inputArea}>
          <input
            type="text"
            className={styles.input}
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button className={styles.sendBtn} onClick={sendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
