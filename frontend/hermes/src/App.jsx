const API_URL = import.meta.env.VITE_BACKEND_API_URL;
const WS_URL = `ws://${API_URL}/chatbot/socket`;

import React, { useState, useEffect, useRef } from "react";


const Chatbot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      from: "bot",
      text:
        "Witaj! Jak mogę pomóc?.",
    },
  ]);
  const [input, setInput] = useState("");
  const ws = useRef(null);
  const messagesEndRef = useRef(null);

  const connectWebSocket = () => {
    ws.current = new WebSocket(WS_URL);

    ws.current.onopen = () => {
      console.log("Connection to WebSocket server established");
    };

    ws.current.onmessage = (event) => {
      const data = event.data;
      setMessages((prev) => [
        ...prev,
        { id: Date.now(), from: "bot", text: data },
      ]);
    };

    ws.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.current.onclose = () => {
      console.log("Disconnected from WebSocket server");
    };
  };

  useEffect(() => {
    connectWebSocket();

    return () => {
      if (ws.current) ws.current.close();
    };
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = () => {
    if (!input.trim()) return;

    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(input);
      setMessages((prev) => [
        ...prev,
        { id: Date.now(), from: "user", text: input },
      ]);
      setInput("");
    } else {
      alert("Connection to WebSocket server is unavailable.");
    }
  };

  // New session
  const startNewSession = () => {
    // Close existing WebSocket connection if it exists
    if (ws.current) {
      ws.current.close();
    }

    // Clear messages
    setMessages([
      {
        id: Date.now(),
        from: "bot",
        text:
          "Witaj! Zacznijmy nową rozmowę.\n\nJak mogę Ci pomóc dzisiaj?",
      },
    ]);

    // Connect to WebSocket again
    setTimeout(() => {
      connectWebSocket();
    }, 500);
  };

  const formatText = (text) => {
    return text.split("\n").map((line, idx) => (
      <React.Fragment key={idx}>
        {line === "" ? <br /> : line}
        <br />
      </React.Fragment>
    ));
  };

  return (
    <div className="fixed bottom-6 right-6 w-80 max-w-full bg-white shadow-lg rounded-xl flex flex-col overflow-hidden font-sans text-gray-800">
      <div className="bg-indigo-600 text-white p-4 font-semibold rounded-t-xl flex justify-between items-center">
        <span>Pomoc Sklepu</span>
        <button
          onClick={startNewSession}
          className="bg-indigo-800 hover:bg-indigo-900 text-sm px-3 py-1 rounded-md transition"
          aria-label="Nowa sesja"
          title="Rozpocznij nową sesję"
        >
          Nowa sesja
        </button>
      </div>
      <div className="flex-1 p-4 space-y-3 overflow-y-auto max-h-96 scrollbar-thin scrollbar-thumb-indigo-400">
        {messages.map(({ id, from, text }) => (
          <div
            key={id}
            className={`flex ${from === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[70%] px-4 py-2 rounded-xl whitespace-pre-wrap ${
                from === "user"
                  ? "bg-indigo-500 text-white rounded-br-none"
                  : "bg-gray-100 text-gray-900 rounded-bl-none"
              }`}
            >
              {formatText(text)}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-3 border-t border-gray-200 flex items-center gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Napisz wiadomość..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          className="flex-1 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <button
          onClick={sendMessage}
          className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition"
          aria-label="Wyślij"
        >
          Wyślij
        </button>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <div className="h-screen bg-gray-50">
      <Chatbot />
    </div>
  );
}
