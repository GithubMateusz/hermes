import {Header} from "../components/Header/Header.jsx";
import {Outlet} from "react-router-dom";
import {Chatbot} from "../components/Chatbot/Chatbot.jsx";

export const Layout = () => {
    const headers = [
        {name: "Nowości"},
        {name: "T-Shirty"},
        {name: "Sukienki"},
        {name: "Spódnice"},
        {name: "Spodnie"},
        {name: "Body"},
        {name: "Koszule"},
    ];
    return (
        <div className="flex flex-col min-h-screen font-inria">
            <Header items={
                headers
            }/>
            <main className="py-10 bg-[#E8D4CC54]/33">
                <div className="flex-1 container mx-auto ">
                    <Outlet/>
                </div>
            </main>
            <Chatbot/>
        </div>
    );
};
