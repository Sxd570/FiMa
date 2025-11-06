import { useEffect, useState, useRef } from "react";

export default function Penny() {
  const [input, setInput] = useState("");
  const [userMessages, setUserMessages] = useState([]);
  const [agentResponses, setAgentResponses] = useState({
    orchestrator: [],
    agent_api: [],
    ui_smith: [],
  });

  const wsRef = useRef(null);
  const reconnectTimer = useRef(null);
  const currentResponses = useRef({
    orchestrator: "",
    agent_api: "",
    ui_smith: "",
  });

  // WebSocket setup
  const connectWebSocket = () => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket("ws://localhost:8001/penny/v1/ws/123/chat");
    wsRef.current = ws;

    ws.onopen = () => console.log("✅ WebSocket connected");

    ws.onclose = (e) => {
      console.warn("⚠️ WebSocket closed. Reconnecting in 2s...", e.reason);
      reconnectTimer.current = setTimeout(connectWebSocket, 2000);
    };

    ws.onerror = (e) => console.error("❌ WebSocket error:", e);

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        const agent = msg.agent || "orchestrator";

        // Initialize agent if missing
        if (!currentResponses.current[agent])
          currentResponses.current[agent] = "";

        // --- Start of new response ---
        if (msg.type === "response_start") {
          currentResponses.current[agent] = "";
          setAgentResponses((prev) => ({
            ...prev,
            [agent]: [
              ...prev[agent],
              { text: "", isStreaming: true },
            ],
          }));
        }

        // --- Streaming chunks ---
        else if (msg.type === "chunk") {
          const chunk = msg.data?.replace(/<\/think>/g, "</think>\n") || "";
          currentResponses.current[agent] += chunk;

          setAgentResponses((prev) => {
            const updated = { ...prev };
            const msgs = [...(updated[agent] || [])];
            if (!msgs.length || !msgs[msgs.length - 1].isStreaming) {
              msgs.push({ text: chunk, isStreaming: true });
            } else {
              msgs[msgs.length - 1].text = currentResponses.current[agent];
            }
            updated[agent] = msgs;
            return updated;
          });
        }

        // --- End of response ---
        else if (msg.type === "response_end") {
          setAgentResponses((prev) => {
            const updated = { ...prev };
            const msgs = [...(updated[agent] || [])];
            const last = msgs[msgs.length - 1];
            if (last) last.isStreaming = false;
            updated[agent] = msgs;
            return updated;
          });
          currentResponses.current[agent] = "";
        }
      } catch {
        console.log("Non-JSON message:", event.data);
      }
    };
  };

  // Mount WebSocket
  useEffect(() => {
    connectWebSocket();
    return () => clearTimeout(reconnectTimer.current);
  }, []);

  // Send message
  const sendMessage = () => {
    if (!input.trim()) return;

    // Add user message to user messages box
    setUserMessages((prev) => [...prev, input]);

    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(input);
      setInput("");
    } else {
      console.warn("WebSocket not open. Reconnecting...");
      connectWebSocket();
      setTimeout(() => wsRef.current?.send(input), 500);
    }
  };

  const formatResponse = (text) => {
    if (!text) return "";
    const thinkMatch = text.match(/<think>([\s\S]*?)<\/think>/);
    if (thinkMatch) {
      const thinkContent = thinkMatch[1].trim();
      const visibleContent = text.split("</think>").pop().trim();
      return (
        <div>
          <div className="text-gray-500 text-sm italic border-l-2 border-gray-300 pl-2 mb-1 whitespace-pre-wrap">
            🤔 {thinkContent}
          </div>
          <div className="whitespace-pre-wrap">{visibleContent}</div>
        </div>
      );
    }
    return <div className="whitespace-pre-wrap">{text}</div>;
  };

  const UserMessageBox = () => {
    const containerRef = useRef(null);
    useEffect(() => {
      if (containerRef.current)
        containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }, [userMessages]);

    return (
      <div className="flex flex-col w-1/4 border rounded-lg p-3 bg-white shadow-sm border-gray-300">
        <h2 className="text-lg font-semibold mb-2 text-center text-gray-700">
          Your Messages
        </h2>
        <div
          ref={containerRef}
          className="flex-1 overflow-y-auto space-y-2 mb-2 border rounded-lg p-2 bg-gray-50"
        >
          {userMessages.length === 0 ? (
            <div className="text-gray-400 text-sm text-center">
              No messages yet
            </div>
          ) : (
            userMessages.map((msg, i) => (
              <div
                key={i}
                className="p-2 rounded-lg bg-blue-100 text-left"
              >
                <div className="whitespace-pre-wrap">{msg}</div>
              </div>
            ))
          )}
        </div>
      </div>
    );
  };

  const AgentResponseBox = ({ agentName, responses, color }) => {
    const containerRef = useRef(null);
    useEffect(() => {
      if (containerRef.current)
        containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }, [responses]);

    return (
      <div
        className={`flex flex-col w-1/4 border rounded-lg p-3 bg-white shadow-sm border-${color}-300`}
      >
        <h2
          className={`text-lg font-semibold mb-2 text-center capitalize text-${color}-700`}
        >
          {agentName.replace("_", " ")}
        </h2>
        <div
          ref={containerRef}
          className="flex-1 overflow-y-auto space-y-2 mb-2 border rounded-lg p-2 bg-gray-50"
        >
          {responses.length === 0 ? (
            <div className="text-gray-400 text-sm text-center">
              No responses yet
            </div>
          ) : (
            responses.map((response, i) => (
              <div
                key={i}
                className={`p-2 rounded-lg bg-${color}-50 text-left`}
              >
                {formatResponse(response.text || "")}
              </div>
            ))
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="h-screen flex flex-col">
      {/* 4 Boxes: User Messages + 3 Agent Response Boxes */}
      <div className="flex flex-1 gap-3 p-4 bg-gray-100">
        <UserMessageBox />
        <AgentResponseBox
          agentName="orchestrator"
          color="blue"
          responses={agentResponses.orchestrator}
        />
        <AgentResponseBox
          agentName="agent_api"
          color="green"
          responses={agentResponses.agent_api}
        />
        <AgentResponseBox
          agentName="ui_smith"
          color="purple"
          responses={agentResponses.ui_smith}
        />
      </div>

      {/* Input */}
      <div className="flex p-4 border-t gap-2 bg-white">
        <input
          type="text"
          className="flex-1 border rounded-lg p-2"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          onClick={sendMessage}
          className="bg-blue-500 text-white px-4 rounded-lg hover:bg-blue-600"
        >
          Send
        </button>
      </div>
    </div>
  );
}