import { useState, useEffect, useRef } from "react";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const wsRef = useRef(null);
  const chatEndRef = useRef(null);

  // Function to extract JSX code from custom markers
  const extractJSXCode = (text) => {
    const startMarker = 'CUSTOM_COMPONENT_START';
    const endMarker = 'CUSTOM_COMPONENT_END';
    
    const startIndex = text.indexOf(startMarker);
    const endIndex = text.indexOf(endMarker);
    
    if (startIndex !== -1 && endIndex !== -1) {
      const jsxCode = text.substring(
        startIndex + startMarker.length, 
        endIndex
      ).trim();
      
      const beforeCode = text.substring(0, startIndex).trim();
      const afterCode = text.substring(endIndex + endMarker.length).trim();
      
      return {
        hasJSX: true,
        jsxCode,
        beforeText: beforeCode,
        afterText: afterCode,
        fullText: text
      };
    }
    
    return {
      hasJSX: false,
      jsxCode: null,
      beforeText: text,
      afterText: '',
      fullText: text
    };
  };

  // Component to render JSX code with syntax highlighting
  const CodeBlock = ({ code }) => (
    <div className="mt-3 bg-gray-800 text-green-400 p-4 rounded-lg overflow-x-auto">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-gray-400">JSX Component</span>
        <button 
          className="text-xs bg-blue-600 hover:bg-blue-700 px-2 py-1 rounded text-white"
          onClick={() => navigator.clipboard.writeText(code)}
        >
          Copy
        </button>
      </div>
      <pre className="text-sm">
        <code>{code}</code>
      </pre>
    </div>
  );

  // Component to render individual messages
  const MessageBubble = ({ msg, index }) => {
    const parsed = msg.role === "agent" ? extractJSXCode(msg.text) : null;
    
    return (
      <div
        key={index}
        className={`max-w-4xl p-3 rounded-lg ${
          msg.role === "user"
            ? "bg-blue-500 text-white ml-auto"
            : "bg-white text-black border shadow-sm"
        }`}
      >
        {msg.role === "user" ? (
          <div className="whitespace-pre-wrap">{msg.text}</div>
        ) : (
          <div>
            {/* Text before JSX code */}
            {parsed?.beforeText && (
              <div className="whitespace-pre-wrap mb-2">{parsed.beforeText}</div>
            )}
            
            {/* JSX Code Block */}
            {parsed?.hasJSX && (
              <CodeBlock code={parsed.jsxCode} />
            )}
            
            {/* Text after JSX code */}
            {parsed?.afterText && (
              <div className="whitespace-pre-wrap mt-2">{parsed.afterText}</div>
            )}
            
            {/* Fallback for messages without custom markers */}
            {!parsed?.hasJSX && !parsed?.beforeText && (
              <div className="whitespace-pre-wrap">{msg.text}</div>
            )}
          </div>
        )}
      </div>
    );
  };

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");
    wsRef.current = ws;
    let currentResponse = "";

    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);

      if (message.type === "chunk") {
        // Accumulate chunks in a local variable first
        currentResponse += message.data;
        
        setMessages((prev) => {
          const lastMsg = prev[prev.length - 1];
          if (lastMsg && lastMsg.role === "agent") {
            // Replace the entire text with accumulated response
            const updated = [...prev];
            updated[updated.length - 1].text = currentResponse;
            return updated;
          } else {
            // First agent chunk
            return [...prev, { role: "agent", text: currentResponse }];
          }
        });
      } else if (message.type === "response_start") {
        setIsTyping(true);
        currentResponse = ""; // Reset for new response
      } else if (message.type === "response_end") {
        setIsTyping(false);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
    };

    return () => ws.close();
  }, []);

  useEffect(() => {
    // Auto scroll to bottom when messages update
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = () => {
    if (!inputText.trim()) return;

    // Add user message to the chat
    setMessages((prev) => [...prev, { role: "user", text: inputText }]);

    // Send to backend
    wsRef.current.send(
      JSON.stringify({ type: "message", data: inputText })
    );

    setInputText("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b px-4 py-3">
        <h1 className="text-lg font-semibold text-gray-800">React Component Generator</h1>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <MessageBubble key={index} msg={msg} index={index} />
        ))}

        {isTyping && (
          <div className="flex items-center space-x-2 text-gray-500">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
            </div>
            <span className="italic">Generating component...</span>
          </div>
        )}

        <div ref={chatEndRef}></div>
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t">
        <div className="max-w-4xl mx-auto">
          <textarea
            className="w-full p-3 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows="3"
            placeholder="Ask for a React component... (e.g., 'Create a login form' or 'Make a card component')"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyPress}
          />

          <div className="flex justify-between items-center mt-2">
            <span className="text-xs text-gray-500">
              Press Enter to send, Shift+Enter for new line
            </span>
            <button
              className="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              onClick={handleSend}
              disabled={!inputText.trim() || isTyping}
            >
              {isTyping ? "Generating..." : "Send"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}


// import { useState } from "react";
// import JSXParser from "react-jsx-parser";

// export default function ChatInterface() {
//   const [messages, setMessages] = useState([]);
//   const [inputCode, setInputCode] = useState("");

//   const handleSend = () => {
//     if (inputCode.trim()) {
//       setMessages((prev) => [...prev, inputCode]);
//       setInputCode("");
//     }
//   };

//   return (
//     <div className="w-full max-w-2xl mx-auto p-4">
//       <h1 className="text-2xl font-bold mb-4">Dynamic JSX Chat</h1>

//       <div className="border p-4 min-h-[300px] space-y-4 bg-gray-50">
//         {messages.map((code, index) => (
//           <div key={index} className="p-2 border rounded bg-white">
//             <JSXParser
//               bindings={{}}
//               components={[]}
//               jsx={code}
//               renderInWrapper={false}
//             />
//           </div>
//         ))}
//       </div>

//       <textarea
//         className="w-full border rounded p-2 mt-4"
//         rows={10}
//         placeholder="Enter JSX component code here..."
//         value={inputCode}
//         onChange={(e) => setInputCode(e.target.value)}
//       />

//       <button
//         className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
//         onClick={handleSend}
//       >
//         Send
//       </button>
//     </div>
//   );
// }
