import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Table } from '../components/shared/table';
import { Spinner } from '../components/shared/spinner';
import { ErrorMessage, InfoMessage, SuccessMessage } from '../components/shared/displayMessage';
import { Header, headerChoice } from '../components/shared/header';
import { FloatingBtn } from '../components/shared/floatingBtn';
import { staticRoutes } from '../routes/routes';
import { Icontooltip } from '../components/shared/tooltips';
import BusStationRootes from '../routes/api/rootes/busStationRootes';
import { errorHandler } from '../util/errorHandler';

export function BusStationPage() {
    // receive message that pass from create, update and delete 
    const location = useLocation();
    let { successMessage } = location.state || {};

    // for table 
    const colName = ["Station Id", "Station Name"];
    const dataName = ["StationId", "StationName"]; 
    const where = "busStation";

    // use to handle the data to be display 
    const [responses, setResponses] = useState([]);

    const [filters, setFilters] = useState({ 
                                        StationId: "", 
                                        StationName: "",
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
            const response = await BusStationRootes.getBusStations(queryParams);

            // set response to responses
            setResponses(response.data);
        } catch (err) {
            errorHandler({err, setErrors});
        } finally {
            // keep track spinner, when responses have success update change the state 
            setIsLoading(false);
            setIsDisabled(false);
        }
    };

    // onchange update 
    const handleChange = (e) => {
        // get target name and values 
        const {name, value} = e.target;
        
        setFilters((prevValues) => ({            
            ...prevValues,
            [name]: value, 
        }));
    };

    const clearFilter = () => {
        setFilters(({
            StationId: "",
            StationName: "",
        }));

        fetchData();
    };

    // filter btn
    const handleSubmit = () => {
        fetchData(filters);
    };

    // initial fecthing when page load
    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div>
            <Header
                who={headerChoice.busStation}
            />
            <div className='p-5' style={{"marginTop" : "70px"}}>
                {/* filter input */}
                <form className='bg-sur-container p-4 rounded-top '>
                    <legend className='text-primary cus-font'><b>STATION MANAGEMENT</b></legend>
                    <div className='row'>
                        {/* bus station id - text */}
                        <div className='col'>
                            <label className="col-form-label ps-1" for="StationId">Station Id :</label>
                            <input type="text" className="form-control fs-cus-1" placeholder="Filter By Station Id" id="StationId" name="StationId" value={filters.StationId} onChange={handleChange} />
                        </div>
                        {/* station name - text */}
                        <div className='col'>
                            <label className="col-form-label ps-1" for="StationName">Station Name :</label>
                            <input type="text" className="form-control fs-cus-1" placeholder="Filter By Station Name" id="StationName" name='StationName' value={filters.StationName} onChange={handleChange} />
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
                link={staticRoutes.busStationCreate}
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