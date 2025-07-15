import HomePage from "../pages/HomePage.jsx";
import {Layout} from "../layout/Layout.jsx";
import {Navigate} from "react-router-dom";

export const routes = [
    {
        path: "/",
        element: (
            <Layout/>
        ),
        children: [
            {
                path: "/home",
                element: <HomePage/>
            },
            {
                index: true,
                element: <Navigate to="/home"/>,
            },
            {
                path: '*',
                element: <Navigate to="/home" replace/>,
            },
        ]
    },
]
