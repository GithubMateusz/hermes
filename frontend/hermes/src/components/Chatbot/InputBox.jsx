import {IoSendOutline} from "react-icons/io5";
import React from "react";

export const InputBox = ({input, setInput, sendMessage}) => {
    return (
        <div className="flex items-center justify-center p-4">
            <div className="flex items-center bg-[#EED7CE] rounded-full p-2 w-75 text-[10px]">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Wpisz pytanie..."
                    onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                    className="bg-transparent flex-1 outline-none placeholder-gray-400"
                />
                <button
                    onClick={sendMessage}
                    className="ml-2 text-gray-700 hover:text-gray-900"
                    aria-label="Wyślij"
                >
                    <IoSendOutline size={16}/>
                </button>
            </div>
        </div>
    )
}
