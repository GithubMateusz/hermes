import React from "react";

export const formatText = (text) => {
    return text.split("\n").map((line, idx) => (
        <React.Fragment key={idx}>
            {line === "" ? <br/> : line}
            <br/>
        </React.Fragment>
    ));
};
