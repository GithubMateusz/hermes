import React from "react";
import {formatText} from "../../helpers/text.jsx";

export const QuestionContainer = ({questions, onQuestionClick}) => {
    return (
        <div className="flex-row space-y-3 self-end">
            {questions.map((question) => (
                <Question key={question.key} text={question.text} onQuestionClick={onQuestionClick}/>
            ))}
        </div>
    );
}

const Question = ({text, onQuestionClick}) => {

    return (
        <div
            className="flex items-center gap-2 justify-end cursor-pointer" onClick={() => {
            onQuestionClick(text);
        }}
        >
            <div
                className="max-w-[70%] px-4 py-2 rounded-xl shadow-lg whitespace-pre-wrap text-[10px] bg-[#B68FBB99]/60"
            >
                {formatText(text)}
            </div>
        </div>
    )
}
