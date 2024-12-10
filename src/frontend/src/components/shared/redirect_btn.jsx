import React from "react";
import { useNavigate } from "react-router-dom";

export function RedirectBtn({ redirectTo, btnContent, btnClass }) {
    const navigate = useNavigate();

    // function
    const handleRedirect = () => {
        // redirect to specific page 
        navigate(redirectTo);
    };

    return (
        <button onClick={handleRedirect} className={btnClass}>{btnContent}</button>
    );
}