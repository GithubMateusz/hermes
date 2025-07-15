import React from "react";
import {formatText} from "../../helpers/text.jsx";


export const MessageContainer = ({messages, messagesEndRef, loadingResponse }) => {
    return (
        <div className="flex-row space-y-3">
            {messages.map((message) => (
                <Message key={message.key} from={message.from} text={formatText(message.text)}/>
            ))}
            {loadingResponse && <Message key="loading" from="bot" text={<Loading/>}/>}
            <div ref={messagesEndRef}/>
        </div>
    );
}

const Message = ({from, text}) => {

    return (
        <div
            className={`flex items-center gap-2 ${from === "user" ? "justify-end" : "justify-start"}`}
        >
            {from === "bot" && <BotIcon/>}
            <div
                className={`max-w-[70%] px-4 py-2 rounded-xl shadow-lg whitespace-pre-wrap text-[10px] ${
                    from === "user"
                        ? "bg-[#B68FBB99]/60"
                        : "bg-[#F0C0C08F]/56"
                }`}
            >
                {text}
            </div>
        </div>
    )
}

const BotIcon = () => {
    return (
        <div className="bg-[#B68FBB99] w-8 h-8 rounded-full">
            <img
                src="/botIcon.png"
                alt="bot-icon"
                className="object-cover object-center"
            />
        </div>
    )
}

const Loading = () => {
    return (
        <div className='flex justify-center items-center'>
            <div className='animate-bounce [animation-delay:-0.3s]'>
                .
            </div>
            <div className='animate-bounce [animation-delay:-0.15s]'>
                .
            </div>
            <div className='animate-bounce'>
                .
            </div>
        </div>
    );
}
