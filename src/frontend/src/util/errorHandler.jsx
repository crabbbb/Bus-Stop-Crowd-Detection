
export function errorHandler({err, setErrors}) {
    // store err in error
    if (err.response) {
        setErrors((prev) => ({
            ...prev,
            responseErrors: `${err.response.statusText}`
        }));
    } else if (err.request) {
        setErrors((prev) => ({
            ...prev,
            requestErrors: "No response from the server. Please try again later"
        }));
    } else {
        setErrors((prev) => ({
            ...prev,
            unexpectedErrors: "An unexpected error occurred"
        }));
    }
}

export function setFormErrorsHandler({err, formErrors, setFormErrors}) {
    // assign value to the form one by one 
    Object.keys(err).map((key) => {
        if (formErrors.hasOwnProperty(key)) {
            setFormErrors((prev) => ({
                ...prev,
                [key]: err[key] || "Unknown error", 
            }));
        }
    })
}