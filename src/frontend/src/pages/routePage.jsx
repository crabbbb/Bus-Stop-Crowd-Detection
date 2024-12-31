import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import RouteRootes from '../routes/api/rootes/routeRootes';
import { Table } from '../components/shared/table';
import { Spinner } from '../components/shared/spinner';
import { ErrorMessage, InfoMessage, SuccessMessage } from '../components/shared/displayMessage';
import { Header, headerChoice } from '../components/shared/header';
import { FloatingBtn } from '../components/shared/floatingBtn';
import { staticRoutes } from '../routes/routes';
import { Icontooltip } from '../components/shared/tooltips';
import { toast, ToastContainer } from "react-toastify";
import { errorHandler } from '../util/errorHandler';
import "react-toastify/dist/ReactToastify.css";

export function RoutePage() {
    // receive message that pass from create, update and delete 
    const location = useLocation();
    let { successMessage } = location.state || {};

    // for table 
    const colName = ["Route Id", "Route Duration", "From Campus", "Status"];
    const dataName = ["RouteId", "RouteDuration", "FromCampus", "IsActive"]; 
    const where = "route";

    // filter button disable 
    const [isDisabled, setIsDisabled] = useState(true);

    // constant value 
    const active = "Active";
    const notactive = "NotActive";

    // spinner 
    const [isLoading, setIsLoading] = useState(false);
    // use to handle the error send back from backend 
    const [errors, setErrors] = useState({
                                    requestErrors: "",
                                    responseErrors: "",
                                    unexpectedErrors: ""
                                });
    // use to handle the data to be display 
    const [responses, setResponses] = useState([]);
    // use to handle the error send bac
    // use to handle the data user fill in in filter 
    const [filters, setFilters] = useState({ 
                                        RouteId: "", 
                                        MinDuration: "",
                                        MaxDuration: "", 
                                        FromCampus: "", 
                                        IsActive: "" 
                                    });
                                    
    const [filtersError, setFiltersError] = useState({ 
                                                MaxDuration: {
                                                    e: false, 
                                                    message: "Maximum Duration can't smaller than the Minimum Duration"
                                                },
                                                MinDuration: {
                                                    e: false, 
                                                    message: "Minimum Duration can't greater than the Maximum Duration"
                                                },
                                            });
    // create function for fetching data from backend 
    const fetchData = async (params = {}) => {
        try {
            // clear out all the previous data 
            setResponses(null);
            setIsLoading(true);
            setErrors(null);
            setIsDisabled(true);

            // send together with filter 
            const queryParams = new URLSearchParams(params).toString();
            const response = await RouteRootes.getRoutess(queryParams);

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
            MaxDuration: {
                ...prev.MaxDuration, 
                e: false,
            }, 
            MinDuration: {
                ...prev.MinDuration,
                e: false,
            },
        }));

        // check min max 
        if (name === "MaxDuration") {
            
            if (filters.MinDuration && value < filters.MinDuration && value > 0) {
                // max smaller than min
                // set the error message 
                setFiltersError((prev) => ({
                    ...prev, 
                    MaxDuration: {
                        ...prev.MaxDuration,
                        e: true,
                    },
                }));
                setIsDisabled(true);
            } else {
                // no error 
                setIsDisabled(false)
            }
            
        } else if (name === "MinDuration") {
            if (filters.MaxDuration && value > filters.MaxDuration) {
                // min greater than max 
                setFiltersError((prev) => ({
                    ...prev,
                    MinDuration: {
                        ...prev.MinDuration,
                        e: true,
                    }
                }))
                setIsDisabled(true);
            } else {
                // no error 
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
            RouteId: "",
            MinDuration: "",
            MaxDuration: "",
            FromCampus: "",
            IsActive: ""
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
                who={headerChoice.route}
            />
            <div className='p-5' style={{"marginTop" : "70px"}}>
                {/* filter input */}
                <form className='bg-sur-container p-4 rounded-top '>
                    <legend className='text-primary cus-font'><b>ROUTE MANAGEMENT</b></legend>
                    <div className='row'>
                        {/* Route id - text */}
                        <div className='col'>
                            <label className="col-form-label ps-1" for="RouteId">Route Id :</label>
                            <input type="text" className="form-control fs-cus-1" placeholder="Filter By Route Id" id="RouteId" name="RouteId" value={filters.RouteId} onChange={handleChange} />
                        </div>
                        {/* From Campus */}
                        <div className='col'>
                            <label className="col-form-label ps-1" for="FormCampus">Route Duration Time <Icontooltip icon={"bi-info-circle-fill"} content={"Duration MUST BE greater than 0"}/> : </label>
                            <div className="d-flex">
                                <input type="number" className={`form-control fs-cus-1 ${"is-valid" ? filtersError.MinDuration.e : ""}`}  placeholder="Minimum Duration Time" id="MinDuration" name='MinDuration' min={0} value={filters.MinDuration} onChange={handleChange} onKeyDown={(e) => {
                                    if (e.key === "-" || e.key === ".") {
                                        // prevent user type negative value
                                        e.preventDefault();
                                    }
                                }} />
                                <span className="ms-1 me-1 align-bottom">-</span>
                                {/* max */}
                                <input type="number" className={`form-control fs-cus-1 ${"is-valid" ? filtersError.MaxDuration.e : ""}`} placeholder="Maximum Duration Time" id="MaxDuration" name='MaxDuration' min={0} value={filters.MaxDuration} onChange={handleChange} onKeyDown={(e) => {
                                    if (e.key === "-" || e.key === ".") {
                                        // prevent user type negative value
                                        e.preventDefault();
                                    }
                                }} />
                            </div>
                            {/* error message for wrong capacity */}
                            <div className={`fs-cus-1 p-1 text-danger ${ filtersError.MaxDuration.e ? "" : filtersError.MinDuration.e ? "" : "visually-hidden"}`}>{filtersError.MinDuration.message}</div>
                        </div>
                    </div>
                    <div className='row'>
                        {/* carplate - text */}
                        <div className='col'>
                            <label className="col-form-label ps-1" for="FromCampus">From Campus <Icontooltip icon={"bi-info-circle-fill"} content={"First Station start at campus. Only routes marked From campus will carry passengers from the campus bus stop"}/> :</label>
                            <select className="form-select fs-cus-1" id="FromCampus" name='FromCampus' value={filters.FromCampus} onChange={handleChange}>
                                <option value={""}>-</option>
                                <option value={0}>{"Yes"}</option>
                                <option value={1}>{"No"}</option>
                            </select>
                        </div>
                        {/* is active - checklist */}
                        <div className='col'>
                            <label for="IsActive" className="col-form-label ps-1">Bus Status :</label>
                            <select className="form-select fs-cus-1" id="IsActive" name='IsActive' value={filters.IsActive} onChange={handleChange}>
                                <option value={""}>-</option>
                                <option value={0}>{active}</option>
                                <option value={1}>{notactive}</option>
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
                link={staticRoutes.routeCreate}
            />
            <ToastContainer 
                position="top-right"
                autoClose={5000} // 5 seconds
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
            />
        </div>
        );
}