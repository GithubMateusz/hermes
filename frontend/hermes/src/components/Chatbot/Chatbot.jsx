import React, {useEffect, useRef} from "react";
import {MessageContainer} from "./Message.jsx";
import {InputBox} from "./InputBox.jsx";
import {useChatbot} from "../../hooks/useChatbot.jsx";
import {WS_URL} from "../../api/chatbotApi.jsx";
import {QuestionContainer} from "./Question.jsx";


const questions = [
    {
        key: "1",
        text: "Jakie są dostępne opcje dostawy?",
    },
    {
        key: "2",
        text: "Jak mogę śledzić moje zamówienie?",
    },
    {
        key: "3",
        text: "Ile mam czasu na zwrot produktów?",
    }
]

export const Chatbot = () => {
    const {
        messages,
        input,
        setInput,
        loadingResponse,
        showQuestions,
        sendMessage,
        startNewSession,
    } = useChatbot(WS_URL);

    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({behavior: "smooth"});
    }, [messages]);


    const onQuestionClick = (text) => {
        setInput(text);
        sendMessage();
    }

    return (
        <div
            className="fixed bottom-10 right-12 h-100 w-80 max-w-full bg-white shadow-xl rounded-xl flex flex-col overflow-auto text-gray-800">
            <Header startNewSession={startNewSession}/>
            <div className="flex flex-col justify-between flex-1 p-4 overflow-y-auto max-h-96 scrollbar-thin scrollbar-thumb-indigo-400 content-end">
                <MessageContainer messages={messages} messagesEndRef={messagesEndRef}
                                  loadingResponse={loadingResponse}/>
                {showQuestions && <QuestionContainer questions={questions} onQuestionClick={onQuestionClick}/>}
            </div>
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
                onClick={() => {
                    startNewSession()
                }}
                className="bg-[#EED7CE] hover:bg-[#AC83B7] text-sm px-3 py-1 rounded-md transition"
                aria-label="Nowa sesja"
                title="Rozpocznij nową sesję"
            >
                Nowa sesja
            </button>
        </div>
    )
}
