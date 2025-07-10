import React, {useEffect, useRef} from "react";
import {MessageContainer} from "./Message.jsx";
import {InputBox} from "./InputBox.jsx";
import {useChatbot} from "../../hooks/useChatbot.jsx";
import {WS_URL} from "../../api/chatbotApi.jsx";




export const Chatbot = () => {
    const {
        messages,
        input,
        setInput,
        loadingResponse,
        sendMessage,
        startNewSession,
    } = useChatbot(WS_URL);

    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({behavior: "smooth"});
    }, [messages]);

    return (
        <div
            className="fixed bottom-10 right-12 h-100 w-80 max-w-full bg-white shadow-xl rounded-xl flex flex-col overflow-hidden text-gray-800">
            <Header startNewSession={startNewSession}/>
            <MessageContainer messages={messages} messagesEndRef={messagesEndRef} loadingResponse={loadingResponse}/>
            <InputBox input={input} setInput={setInput} sendMessage={sendMessage}/>
        </div>
    );
};

const Header = ({startNewSession}) => {
    return (
        <div
            className="bg-gradient-to-r from-[#EED7CE] to-[#AC83B7] p-4 flex justify-between items-center shadow-xl  border-1 border-[#DDDDDD]">
            <span className="text-2xl font-light">Chatbot</span>
            <button
                onClick={startNewSession}
                className="bg-[#EED7CE] hover:bg-[#AC83B7] text-sm px-3 py-1 rounded-md transition"
                aria-label="Nowa sesja"
                title="Rozpocznij nową sesję"
            >
                Nowa sesja
            </button>
        </div>
    )
}
