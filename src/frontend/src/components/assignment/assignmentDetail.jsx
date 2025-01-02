import React, { useState, useEffect, useRef } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import { Header, headerChoice } from "../shared/header";
import { Spinner } from "../shared/spinner";
import { SuccessMessage, ErrorMessage } from "../shared/displayMessage";
import AssignmentRootes from "../../routes/api/rootes/assignmentRootes";
import { AssignmentForm } from "./assignmentForm";
import { errorHandler } from "../../util/errorHandler";
import { UseNavigateIfSuccess, UseNavigateIfNotFound } from "../../util/navigatePage";

export function AssignmentDetail() {
    const { id } = useParams();
    const navigate = useNavigate();

    // 2) Possibly get "successMessage" from navigation state (if any)
    const location = useLocation();
    const { successMessage } = location.state || {};
    
    const navigateIfSuccess = UseNavigateIfSuccess();
    const navigateIfNotFound = UseNavigateIfNotFound();
    

    // 3) State for assignment data
    //    We store: Time, DayOfWeek, BusId (as {value,label}), RouteId (as {value,label})
    const [form, setForm] = useState({
                                    AssignmentId: "",
                                    Time: "",
                                    DayOfWeek: "1",  // default Monday
                                    BusId: null,     // {value:"B001", label:"B001 > plate"} or null
                                    RouteId: null
                                });
    const [formErrors, setFormErrors] = useState({
                                            Time: "",
                                            DayOfWeek: "",
                                            BusId: "",
                                            RouteId: ""
                                        });
    const [errors, setErrors] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const [forceDisabled, setForceDisabled] = useState(false);

    // 4) On mount, fetch assignment data from server
    const fetchData = async () => {
        setIsLoading(true);
        setErrors({});
        try {
            const response = await AssignmentRootes.getAssignment(id); 

            const assignment = response.data; 

            setForm({
                AssignmentId: assignment.AssignmentId,
                Time: assignment.Time,                // e.g. "08:00:00"
                DayOfWeek: String(assignment.DayOfWeek), // e.g. "2"
                BusId: assignment.BusId ? { value: assignment.BusId, label: assignment.BusId } : null,
                RouteId: assignment.RouteId ? { value: assignment.RouteId, label: assignment.RouteId } : null
            });
        } catch (err) {
            errorHandler({err, setErrors})
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        // Optionally set up SSE or websockets if you want real-time updates
    }, [id]);

    // 5) Handle “Update” submission
    const handleUpdate = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setErrors({});
        try {
            // Transform your state to raw strings for the server
            const requestData = {
                Time: form.Time, 
                DayOfWeek: form.DayOfWeek,
                BusId: form.BusId ? form.BusId.value : null,
                RouteId: form.RouteId ? form.RouteId.value : null
            };

            const response = await AssignmentRootes.updateAssignment(id, requestData); 

            if (response.status === 200) {
                // success 
                navigate(`/assignment`, {
                state: { successMessage: "Assignment updated successfully!" }
                });
            } 
        } catch (err) {
            errorHandler({err, setErrors})
        } finally {
            setIsLoading(false);
        }
    };

    const handleDelete = async (e) => {
        e.preventDefault();

        // loading start when access to database 
        setIsLoading(true);
        setErrors({});

        try {
            const response = await AssignmentRootes.deleteAssignment(id);

            if (response.status === 200) {
                navigateIfSuccess({response});
            } 
        } catch (err) {
            errorHandler({err, setErrors})
        } finally {
            setIsLoading(false);
        }
    };

    // 7) Handle changes for <input type="time">, <select DayOfWeek>, etc. 
    //    except for BusId & RouteId which are changed by React-Select
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormErrors({ Time: "", DayOfWeek: "", BusId: "", RouteId: "" });

        if (name === "Time") {
            // For example, if user picks "08:00"
            // we might store as "08:00:00"
            const hhmmss = value.length === 5 ? `${value}:00` : value; 
            setForm((prev) => ({ ...prev, Time: hhmmss }));
        } else {
            setForm((prev) => ({ ...prev, [name]: value }));
        }
    };

    return (
        <div>
            <Header who={headerChoice.assignment} />
            <div style={{ height: "600px", marginTop: "100px" }}>
                {isLoading ? (
                    <Spinner />
                ) : Object.keys(errors).length > 0 ? (
                    <ErrorMessage err={errors} />
                ) : (
                <div>
                    {successMessage && <SuccessMessage message={successMessage} />}
                    <AssignmentForm
                        isCreate={false}
                        form={form}
                        formErrors={formErrors}
                        setForm={setForm}
                        handleSubmit={handleUpdate}
                        handleChange={handleChange}
                        handleDelete={handleDelete}
                        isDisabled={false}
                        forceDisaled={forceDisabled}
                    />
                </div>
                )}
            </div>
        </div>
    );
}
