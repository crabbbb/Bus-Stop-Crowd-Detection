import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Header, headerChoice } from "../shared/header";
import { Spinner } from "../shared/spinner";
import { ErrorMessage } from "../shared/displayMessage";
import AssignmentRootes from "../../routes/api/rootes/assignmentRootes";
import { AssignmentForm } from "./assignmentForm";

export function AssignmentCreate() {
    const navigate = useNavigate();

    const [errors, setErrors] = useState({});
    const [formErrors, setFormErrors] = useState({ Time: "", DayOfWeek: "", BusId: "", RouteId: "" });
    const [isLoading, setIsLoading] = useState(false);
    const [isDisabled, setIsDisabled] = useState(false);

    // This is the crucial part—match the server fields exactly:
    // "Time", "DayOfWeek", "BusId", "RouteId"
    const [form, setForm] = useState({
        Time: "",        // e.g. "08:00:00"
        DayOfWeek: "1",  // or 1 if you prefer an integer
        BusId: null,     // will store a React-Select { value, label } for the bus
        RouteId: null,   // will store a React-Select { value, label } for the route
    });

    // handleChange for <input type="time" /> and <select> (DayOfWeek)
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormErrors({ Time: "", DayOfWeek: "", BusId: "", RouteId: "" });
        setIsDisabled(false);

        // If your backend wants HH:MM:SS, we can parse it to that format:
        if (name === "Time") {
        // Value might be "08:15"
        const isoString = new Date(`1970-01-01T${value}:00`).toISOString(); 
        const hhmmss = isoString.substring(11, 19); // "08:15:00"
        setForm((prev) => ({ ...prev, Time: hhmmss }));
        } else {
        // e.g. DayOfWeek
        setForm((prev) => ({ ...prev, [name]: value }));
        }
    };

    // Here is the function that calls your Assignment POST route
    const handleSubmit = async (e) => {
        e.preventDefault();

        // We must send the *raw* strings/IDs to the backend:
        // form.BusId will be { value: "B001", label: "B001 > ABC123" } if using React-Select.
        // So we have to transform them:
        const requestData = {
        Time: form.Time, 
        DayOfWeek: form.DayOfWeek,
        BusId: form.BusId ? form.BusId.value : null, 
        RouteId: form.RouteId ? form.RouteId.value : null
        };

        try {
        setIsLoading(true);

        const response = await AssignmentRootes.createAssignment(requestData);

        // If your Django returns a 201 + the new assignment data in response.data
        // you can redirect or do something like:
        if (response.status === 201) {
            // success
            navigate("/assignment", { state: { successMessage: "Assignment created successfully" } });
        }
        } catch (err) {
        // If the server returns 400 with { error: "some message" }
        // or if you want to handle form validation errors, do so here:
        if (err.response) {
            console.log("Server error:", err.response.data);
            setErrors({ serverError: err.response.data.error || "Unknown error" });
        } else {
            setErrors({ requestError: "Failed to connect to server" });
        }
        } finally {
        setIsLoading(false);
        }
    };

    return (
        <div>
        <Header who={headerChoice.bus} />
        <div style={{ height: "600px", marginTop: "100px" }}>
            {isLoading ? (
            <Spinner />
            ) : Object.keys(errors).length > 0 ? (
            <div className="ps-5 pe-5">
                <ErrorMessage err={errors} />
            </div>
            ) : null}

            <AssignmentForm
                isCreate={true}
                form={form}
                formErrors={formErrors}
                setForm={setForm}
                handleSubmit={handleSubmit}
                handleChange={handleChange}
                isDisabled={isDisabled}
            />
        </div>
        </div>
    );
}
