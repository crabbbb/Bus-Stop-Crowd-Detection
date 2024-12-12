import React, { useEffect, useState } from 'react';
import BusRootes from '../../routes/api/rootes/bus_rootes';
import bus_schedule from '../../routes/api/bus_schedule';
import axios from 'axios';
import { RedirectBtn } from '../shared/redirect_btn';
import { dynamicRoutes } from '../../routes/routes';

export function BusDisplay() {
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
    const [errors, setErrors] = useState([])

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
            setErrors(null);
            setIsLoading(true);

            // send together with filter 
            const queryParams = new URLSearchParams(params).toString();
            // const response = await axios.get(`http://127.0.0.1:8000/busSchedule/bus?${queryParams}`);
            const response = await BusRootes.getBuss(queryParams);

            // set response to responses
            setResponses(response.data);
        } catch (err) {
            // store err in error
            if (err.response) {
                setErrors(`Error ${err.response.status}: ${err.response.statusText}`);
            } else if (err.request) {
                setErrors("No response from the server. Please try again later.");
            } else {
                setErrors("An unexpected error occurred.");
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
            if (filters.MinCapacity && value < filters.MinCapacity) {
                // max smaller than min
                console.log("hello max")
                
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
                console.log("hello min")

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


    return (
        <div className='p-4'>
            {/* filter input */}
            <form className='bg-sur-container p-4 rounded-top'>
                <legend className='text-primary cus-font'><b>BUS MANAGEMENT</b></legend>
                <div className='row'>
                    {/* bus id - text */}
                    <div className='col'>
                        <label class="col-form-label ps-1" for="BusId">Bus Id :</label>
                        <input type="text" className="form-control fs-cus-1" placeholder="Filter By Bus Id" id="BusId" name="BusId" value={filters.BusId} onChange={handleChange} />
                    </div>
                    {/* capacity */}
                    <div className='col'>
                        <label class="col-form-label ps-1" for="Capacity">Bus Capacity <span class="badge bg-warning">(Must greater than 0)</span> : </label>
                        <div className="d-flex">
                            <input type="number" class="form-control fs-cus-1" placeholder="Minimum Capacity" id="MinCapacity" name='MinCapacity' min={0} value={filters.MinCapacity} onChange={handleChange} onKeyDown={(e) => {
                                if (e.key === "-") {
                                    // prevent user type negative value
                                    e.preventDefault();
                                }
                            }} />
                            <span className="ms-1 me-1 align-bottom">-</span>
                            {/* max */}
                            <input type="number" class="form-control fs-cus-1" placeholder="Maximum Capacity" id="MaxCapacity" name='MaxCapacity' min={0} value={filters.MaxCapacity} onChange={handleChange} onKeyDown={(e) => {
                                if (e.key === "-") {
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
                        <label class="col-form-label ps-1" for="CarPlateNo">Car Plate No. :</label>
                        <input type="text" class="form-control fs-cus-1" placeholder="Filter By Car Plate No" id="CarPlateNo" name='CarPlateNo' value={filters.CarPlateNo} onChange={handleChange} />
                    </div>
                    {/* is active - checklist */}
                    <div className='col'>
                        <label for="IsActive" class="col-form-label ps-1">Bus Status :</label>
                        <select class="form-select fs-cus-1" id="IsActive" name='IsActive' value={filters.IsActive} onChange={handleChange}>
                            <option>-</option>
                            <option value={0}>{active}</option>
                            <option value={1}>{notactive}</option>
                        </select>
                    </div>
                </div>
                <div className='row text-end d-flex justify-content-end mt-4'>
                    <div className='w-50'>
                        <button type="button" className="btn btn-warning fs-cus-1 w-25 me-2 rounded-pill" onClick={clearFilter}>Clear</button>
                        <button type="button" className={`btn ${isDisabled ? "btn-grey" : "btn-info"} fs-cus-1 w-25 me-3 rounded-pill `} disabled={isDisabled} onClick={handleSubmit}>Filter</button>
                    </div>
                </div>
            </form>
            {isLoading ? (
                <div className='w-100 text-center row align-items-center justify-content-center' style={{"height": "100px"}}>
                    <div class="spinner-grow text-primary me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="spinner-grow text-success me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="spinner-grow text-secondary me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
            ) : errors ? (
                <p style={{ color: "red" }}>{errors}</p>
            ) : responses && responses.length > 0 ? (
                // have data 
                <table class="table mt-4 text-center">
                    <thead>
                        <tr>
                        <th scope="col">Bus Id</th>
                        <th scope="col">Car Plate No</th>
                        <th scope="col">Capacity</th>
                        <th scope="col">Bus Status</th>
                        <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {responses.map((bus) => (
                            <tr scope="row" key={bus.BusId}>
                                <td>{bus["BusId"]}</td>
                                <td>{bus["Capacity"]}</td>
                                <td>{bus["CarPlateNo"]}</td>
                                <td>{bus["IsActive"] === 0 ? "✅" : "❌"}</td>
                                <td>
                                    {/* btn */}
                                    <RedirectBtn
                                        redirectTo={dynamicRoutes.busDetail(bus["BusId"])}
                                        btnContent="OBJECT DETECTION"
                                        btnClass="btn btn-secondary m-4 w-50 h-75 cus-font"
                                    />
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                // success load but dont have data 
                <p>No Record Found</p>
            )}
            </div>
        );
}