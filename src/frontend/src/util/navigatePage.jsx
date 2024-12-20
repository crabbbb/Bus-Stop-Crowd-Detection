import { useNavigate } from "react-router-dom";

// Custom hook for success navigation
export function UseNavigateIfSuccess() {
    const navigate = useNavigate();

    return ({ response }) => {
        const message = response.data.success;
        const redirect = response.data.redirect;

        // Perform navigation
        navigate(redirect, { state: { successMessage: message } });
    };
}

// Custom hook for not found navigation
export function UseNavigateIfNotFound() {
    const navigate = useNavigate();

    return ({ err }) => {
        navigate("/*", { state: { message: err.response.data.error } });
    };
}
