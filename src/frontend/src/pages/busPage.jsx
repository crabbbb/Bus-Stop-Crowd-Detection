import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import BusRootes from '../routes/api/rootes/busRootes';
import { Table } from '../components/shared/table';
import { Spinner } from '../components/shared/spinner';
import { ErrorMessage, InfoMessage, SuccessMessage } from '../components/shared/displayMessage';
import { Header, headerChoice } from '../components/shared/header';
import { FloatingBtn } from '../components/shared/floatingBtn';
import { staticRoutes } from '../routes/routes';
import { Icontooltip } from '../components/shared/tooltips';
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export function BusPage() {
    // receive message that pass from create, update and delete 
    const location = useLocation();
    let { successMessage } = location.state || {};

    // for table 
    const colName = ["Bus Id", "Car Plate No", "Capacity", "Bus Status"];
    const dataName = ["BusId", "CarPlateNo", "Capacity", "IsActive"]; 
    const where = "bus";

    // use to handle the data to be display 
    const [responses, setResponses] = useState([]);
    // use to handle the error send bac
    // use to handle the data user fill in in filter 
    const [filters, setFilters] = useState({ 
                                        BusId: "", 
                                        MinCapacity: "",
                                        MaxCapacity: "", 
                                        CarPlateNo: "", 
                                        IsActive: "" 
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
                                                    MaxCapacity: {
                                                        e: false, 
                                                        message: "Maximum Capacity can't smaller than the Minimum Capacity"
                                                    },
                                                    MinCapacity: {
                                                        e: false, 
                                                        message: "Minimum Capacity can't greater than the Maximum Capacity"
                                                    },
                                                });

    // constant value 
    const active = "Active";
    const notactive = "NotActive";
    
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
            const response = await BusRootes.getBuss(queryParams);

            // set response to responses
            setResponses(response.data);
        } catch (err) {
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
            MaxCapacity: {
                ...prev.MaxCapacity, 
                e: false,
            }, 
            MinCapacity: {
                ...prev.MinCapacity,
                e: false,
            },
        }));

        // check min max 
        if (name === "MaxCapacity") {
            
            if (filters.MinCapacity && value < filters.MinCapacity && value > 0) {
                // max smaller than min
                // set the error message 
                setFiltersError((prev) => ({
                    ...prev, 
                    MaxCapacity: {
                        ...prev.MaxCapacity,
                        e: true,
                    },
                }));
                setIsDisabled(true);
            } else {
                // no error 
                setIsDisabled(false)
            }
            
        } else if (name === "MinCapacity") {
            if (filters.MaxCapacity && value > filters.MaxCapacity) {
                // min greater than max 
                setFiltersError((prev) => ({
                    ...prev,
                    MinCapacity: {
                        ...prev.MinCapacity,
                        e: true,
                    }
                }))
                setIsDisabled(true);
            } else {
                // no error 
                setIsDisabled(false);
            } 
        }
        
        // ignore other 
        // prevValues = current state / the data that currently store inside the filter 
        // [name]: value is current data 
        // ...prevValues = the other data that not include the target name 
        // ensure the data will be update but at the sametime wont remove the old value 
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
            BusId: "",
            MinCapacity: "",
            MaxCapacity: "",
            CarPlateNo: "",
            IsActive: ""
        }));

        fetchData();
    };

    // initial fecthing when page load
    useEffect(() => {
        fetchData();
    }, []);

    useEffect(() => {
        const eventSource = new EventSource("http://127.0.0.1:8000/busSchedule/busMonitor/");

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const operationType = data.operationType;
            let fullDocument = data.fullDocument;
            if (operationType === "delete") {
                fullDocument = data.documentKey;
            }

            toast.info("Bus record have changed ! Please refresh to get the latest value");
        };

        eventSource.onerror = (error) => {
            console.error("EventSource error:", error);
            eventSource.close(); // Close the connection if there's an error
        };

        return () => eventSource.close();
    }, []);

    return (
        <div>
            <Header
                who={headerChoice.bus}
            />
            <div className='p-5' style={{"marginTop" : "70px"}}>
                {/* filter input */}
                <form className='bg-sur-container p-4 rounded-top '>
                    <legend className='text-primary cus-font'><b>BUS MANAGEMENT</b></legend>
                    <div className='row'>
                        {/* bus id - text */}
                        <div className='col'>
                            <label className="col-form-label ps-1" for="BusId">Bus Id :</label>
                            <input type="text" className="form-control fs-cus-1" placeholder="Filter By Bus Id" id="BusId" name="BusId" value={filters.BusId} onChange={handleChange} />
                        </div>
                        {/* capacity */}
                        <div className='col'>
                            <label className="col-form-label ps-1" for="Capacity">Bus Capacity <Icontooltip icon={"bi-info-circle-fill"} content={"Capacity MUST BE greater than 0"}/> : </label>
                            <div className="d-flex">
                                <input type="number" className={`form-control fs-cus-1 ${filtersError.MinCapacity.e ? "is-invalid" : ""}`}  placeholder="Minimum Capacity" id="MinCapacity" name='MinCapacity' min={0} value={filters.MinCapacity} onChange={handleChange} onKeyDown={(e) => {
                                    if (e.key === "-" || e.key === ".") {
                                        // prevent user type negative value
                                        e.preventDefault();
                                    }
                                }} />
                                <span className="ms-1 me-1 align-bottom">-</span>
                                {/* max */}
                                <input type="number" className={`form-control fs-cus-1 ${filtersError.MaxCapacity.e ? "is-invalid"  : ""}`} placeholder="Maximum Capacity" id="MaxCapacity" name='MaxCapacity' min={0} value={filters.MaxCapacity} onChange={handleChange} onKeyDown={(e) => {
                                    if (e.key === "-" || e.key === ".") {
                                        // prevent user type negative value
                                        e.preventDefault();
                                    }
                                }} />
                            </div>
                            {/* error message for wrong capacity */}
                            <div className={`fs-cus-1 p-1 text-danger ${ filtersError.MaxCapacity.e ? "" : filtersError.MinCapacity.e ? "" : "visually-hidden"}`}>{filtersError.MinCapacity.message}</div>
                        </div>
                    </div>
                    <div className='row'>
                        {/* carplate - text */}
                        <div className='col'>
                            <label className="col-form-label ps-1" for="CarPlateNo">Car Plate No. :</label>
                            <input type="text" className="form-control fs-cus-1" placeholder="Filter By Car Plate No" id="CarPlateNo" name='CarPlateNo' value={filters.CarPlateNo} onChange={handleChange} />
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
                link={staticRoutes.busCreate}
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