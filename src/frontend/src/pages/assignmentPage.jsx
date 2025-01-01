import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Table } from '../components/shared/table';
import { Spinner } from '../components/shared/spinner';
import { ErrorMessage, InfoMessage, SuccessMessage } from '../components/shared/displayMessage';
import { Header, headerChoice } from '../components/shared/header';
import { FloatingBtn } from '../components/shared/floatingBtn';
import { staticRoutes } from '../routes/routes';
import { Icontooltip } from '../components/shared/tooltips';
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import AssignmentRootes from '../routes/api/rootes/assignmentRootes';
import { errorHandler } from '../util/errorHandler';

export function AssignmentPage() {
    // receive message that pass from create, update and delete 
    const location = useLocation();
    let { successMessage } = location.state || {};

    // for table 
    const colName = ["Assignment Id", "Time", "Day Of Week", "Bus Id", "Route Id"];
    const dataName = ["AssignmentId", "Time", "DayOfWeek", "BusId", "RouteId"]; 
    const where = "assignment";

    // use to handle the data to be display 
    const [responses, setResponses] = useState([]);
    // use to handle the error send bac
    // use to handle the data user fill in in filter 
    const [filters, setFilters] = useState({ 
                                        AssignmentId: "", 
                                        MinTime: "",
                                        MaxTime: "",
                                        DayOfWeek: "", 
                                        BusId: "", 
                                        RouteId: "" 
                                    });
                                    
    // use to handle the error send back from backend 
    const [errors, setErrors] = useState({
                                    requestErrors: "",
                                    responseErrors: "",
                                    unexpectedErrors: ""
                                });

    // spinner 
    const [isLoading, setIsLoading] = useState(true);

    // filter button disable 
    const [isDisabled, setIsDisabled] = useState(true);

    const [filtersError, setFiltersError] = useState({ 
                                                    MaxTime: {
                                                        e: false, 
                                                        message: "Maximum Time can't smaller than the Minimum Time"
                                                    },
                                                    MinTime: {
                                                        e: false, 
                                                        message: "Minimum Time can't greater than the Maximum Time"
                                                    },
                                                });
    
    // create function for fetching data from backend 
    const fetchData = async (params = {}) => {
        try {
            // clear out all the previous data 
            setResponses(null);
            setIsLoading(true);
            setIsDisabled(true);
            setErrors(null);

            // send together with filter 
            const queryParams = new URLSearchParams(params).toString();
            const response = await AssignmentRootes.getAssignments(queryParams);

            // set response to responses
            setResponses(response.data);
        } catch (err) {
            errorHandler({err, setErrors})
        } finally {
            // keep track spinner, when responses have success update change the state 
            setIsLoading(false)
            setIsDisabled(false)
        }
    };

    // onchange update 
    const handleChange = (e) => {
        // get target name and values 
        const {name, value} = e.target;
        
        // reset 
        setFiltersError((prev) => ({
            MaxTime: {
                ...prev.MaxTime, 
                e: false,
            }, 
            MinTime: {
                ...prev.MinTime,
                e: false,
            },
        }));

        if (name === "MaxTime") {
            // Ensure value is a valid time
            const maxTime = new Date(`1970-01-01T${value}:00`); // Convert value to Date object
            const minTime = filters.MinTime ? new Date(`1970-01-01T${filters.MinTime}:00`) : null;
        
            if (minTime && maxTime < minTime) {
                // MaxTime is smaller than MinTime
                setFiltersError((prev) => ({
                    ...prev,
                    MaxTime: {
                        ...prev.MaxTime,
                        e: true,
                    },
                }));
                setIsDisabled(true);
            } else {
                // No error
                setFiltersError((prev) => ({
                    ...prev,
                    MaxTime: {
                        ...prev.MaxTime,
                        e: false,
                    },
                }));
                setIsDisabled(false);
            }
        } else if (name === "MinTime") {
            const minTime = new Date(`1970-01-01T${value}:00`); 
            const maxTime = filters.MaxTime ? new Date(`1970-01-01T${filters.MaxTime}:00`) : null;
        
            if (maxTime && minTime > maxTime) {
                // MinTime is greater than MaxTime
                setFiltersError((prev) => ({
                    ...prev,
                    MinTime: {
                        ...prev.MinTime,
                        e: true,
                    },
                }));
                setIsDisabled(true);
            } else {
                // No error
                setFiltersError((prev) => ({
                    ...prev,
                    MinTime: {
                        ...prev.MinTime,
                        e: false,
                    },
                }));
                setIsDisabled(false);
            }
        }

        setFilters((prevValues) => ({            
            ...prevValues,
            [name]: value, 
        }));
    };

    // filter btn
    const handleSubmit = () => {
        fetchData(filters);
    };

    const clearFilter = () => {
        setFilters(({
            AssignmentId: "", 
            MinTime: "",
            MaxTime: "",
            DayOfWeek: "", 
            BusId: "", 
            RouteId: "" 
        }));

        fetchData();
    };

    // initial fecthing when page load
    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div>
            <Header
                who={headerChoice.assignment}
            />
            <div className='p-5' style={{"marginTop" : "70px"}}>
                {/* filter input */}
                <form className='bg-sur-container p-4 rounded-top '>
                    <legend className='text-primary cus-font'><b>ASSIGNMENT MANAGEMENT</b></legend>
                    <div className='row'>
                        {/* bus id - text */}
                        <div className='col'>
                            <label className="col-form-label ps-1" for="AssignmentId">Assignment Id :</label>
                            <input type="text" className="form-control fs-cus-1" placeholder="Filter By Assignment Id" id="AssignmentId" name="AssignmentId" value={filters.AssignmentId} onChange={handleChange} />
                        </div>
                        {/* time */}
                        <div className='col'>
                            <label className="col-form-label ps-1" for="Time">Time : </label>
                            <div className="d-flex">
                                {/* min */}
                                <input id="MinTime" name='MinTime' type="time" value={filters.MinTime} onChange={handleChange} className={`form-control fs-cus-1 ${filtersError.MinTime.e ? "is-invalid" : ""}`} />
                                <span className="ms-1 me-1 align-bottom">-</span>
                                {/* max */}
                                <input id="MaxTime" name='MaxTime' type="time" value={filters.MaxTime} onChange={handleChange} className={`form-control fs-cus-1 ${filtersError.MaxTime.e ? "is-invalid" : ""}`} />
                            </div>
                            {/* error message for wrong capacity */}
                            <div className={`fs-cus-1 p-1 text-danger ${ filtersError.MaxTime.e ? "" : filtersError.MinTime.e ? "" : "visually-hidden"}`}>{filtersError.MinTime.message}</div>
                        </div>
                    </div>
                    <div className='row'>
                        {/* carplate - text */}
                        <div className='col'>
                            <label className="col-form-label ps-1" for="BusId">Bus Id :</label>
                            <input type="text" className="form-control fs-cus-1" placeholder="Filter By Bus Id" id="BusId" name='BusId' value={filters.BusId} onChange={handleChange} />
                        </div>
                        {/* is active - checklist */}
                        <div className='col'>
                            <label for="DayOfWeek" className="col-form-label ps-1">Day of Week :</label>
                            <select className="form-select fs-cus-1" id="DayOfWeek" name='DayOfWeek' value={filters.DayOfWeek} onChange={handleChange}>
                                <option value={""}>-</option>
                                <option value={1}>MONDAY</option>
                                <option value={2}>TUESDAY</option>
                                <option value={3}>WEDNESDAY</option>
                                <option value={4}>THURSDAY</option>
                                <option value={5}>FRIDAY</option>
                                <option value={6}>SATURDAY</option>
                                <option value={0}>SUNDAY</option>
                            </select>
                        </div>
                    </div>
                    <div className='row text-center text-md-end d-flex justify-content-center justify-content-md-end mt-4'>
                        <div className='w-50'>
                            <button type="button" className="btn btn-warning fs-cus-1 w-25 me-2 rounded-pill" onClick={clearFilter}>Clear</button>
                            <button type="button" className={`btn ${isDisabled ? "btn-grey" : "btn-info"} fs-cus-1 w-25 me-3 rounded-pill `} disabled={isDisabled} onClick={handleSubmit}>Filter</button>
                        </div>
                    </div>
                </form>
                {successMessage && (
                    <>
                        <SuccessMessage 
                            message={successMessage}
                        />
                        {window.history.replaceState({}, '')} 
                    </>
                )}
                {isLoading ? (
                    <Spinner />
                ) : errors ? (
                    // show error message 
                    <ErrorMessage 
                        err={errors}    
                    />
                ) : responses && responses.length > 0 ? (
                    // have data 
                    <Table
                        colName={colName}
                        dataName={dataName}
                        rowData={responses}
                        where={where}
                    />
                ) : (
                    // success load but dont have data 
                    // print no record found by using a div
                    <InfoMessage 
                        message={responses["message"]}
                    />
                )}
            </div>
            <FloatingBtn 
                link={staticRoutes.assignmentCreate}
            />
            {/* <ToastContainer 
                position="top-right"
                autoClose={5000} // 5 seconds
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
            /> */}
        </div>
    );
}