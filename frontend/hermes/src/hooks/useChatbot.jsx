import {useEffect, useRef, useState} from "react";

const defaultMessage = {
    key: "default",
    from: "bot",
    text: "Hej, jestem wirtualnym asystentem, jak mogę Ci pomóc ?",
};

export const useChatbot = (WS_URL) => {
    const [messages, setMessages] = useState([defaultMessage]);
    const [input, setInput] = useState("");
    const ws = useRef(null);
    const [loadingResponse, setLoadingResponse] = useState(false);
    const [showQuestions, setShowQuestions] = useState(true);
    const [send, setSend] = useState(false);

    const connectWebSocket = () => {
        ws.current = new WebSocket(WS_URL);

        ws.current.onopen = () => {
            console.log("Connection to WebSocket server established");
        };

        ws.current.onmessage = (event) => {
            setLoadingResponse(false);
            const data = event.data;
            setMessages((prev) => [
                ...prev,
                {key: Date.now(), from: "bot", text: data},
            ]);
        };

        ws.current.onerror = (error) => {
            setLoadingResponse(false);
            alert("WebSocket error:");
            console.error("WebSocket error:", error);
        };

        ws.current.onclose = () => {
            setLoadingResponse(false);
            console.log("Disconnected from WebSocket server");
        };
    };

    const sendInputMessage = () => {
        if (!send || !input.trim()) return;

        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            setShowQuestions(false);
            setSend(false);
            ws.current.send(input);
            setMessages((prev) => [
                ...prev,
                {key: Date.now(), from: "user", text: input},
            ]);
            setInput("");
            setLoadingResponse(true);
        } else {
            alert("Connection to WebSocket server is unavailable.");
            setLoadingResponse(false);
        }
    };

    useEffect(() => {
        sendInputMessage();
    }, [send, input]);

    const startNewSession = () => {
        if (ws.current) {
            ws.current.close();
        }

        setMessages([defaultMessage]);
        setLoadingResponse(false);
        setShowQuestions(true);
        setSend(false);
        setTimeout(() => {
            connectWebSocket();
        }, 500);
    };

    useEffect(() => {
        connectWebSocket();

        return () => {
            if (ws.current) ws.current.close();
        };
    }, []);

    const sendMessage = () => {
        setSend(true);
    };

    return {
        messages,
        input,
        setInput,
        loadingResponse,
        showQuestions,
        sendMessage,
        startNewSession,
    };
};
