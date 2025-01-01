import React, { useState, useEffect } from "react";
import { useParams, useLocation } from "react-router-dom";
import { UseNavigateIfSuccess, UseNavigateIfNotFound } from "../../util/navigatePage";
import { Header, headerChoice } from "../shared/header";
import { Spinner } from "../shared/spinner";
import { SuccessMessage, ErrorMessage } from "../shared/displayMessage";
import { errorHandler, setFormErrorsHandler } from "../../util/errorHandler";
import RouteRootes from "../../routes/api/rootes/routeRootes";
import { RouteForm } from "./routeForm";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import RouteStationRootes from "../../routes/api/rootes/routeStationRootes";

export function RouteDetail() {
    // get the id from url 
    const {id} = useParams();
    console.log(id)

    // use to get the success 
    const location = useLocation();
    let { successMessage } = location.state || {};

    const navigateIfSuccess = UseNavigateIfSuccess();
    const navigateIfNotFound = UseNavigateIfNotFound();

    // use to handle the data to be display from backend to frontend, init value 
    const [responses, setResponses] = useState({});

    const [objId, setObjId] = useState("");

    // fdrm is for handle the change in the form 
    const [form, setForm] = useState({ 
                                        RouteId: "",
                                        RouteDuration: "", 
                                        FromCampus: "", 
                                        IsActive: 0 
                                    });

    const [formErrors, setFormErrors] = useState({ 
                                                RouteId: "",
                                                RouteDuration: "", 
                                                FromCampus: "", 
                                                IsActive: "" 
                                            });

    // use to handle the error which using 500 + / 400 + response 
    const [errors, setErrors] = useState({});

    // spinner 
    const [isLoading, setIsLoading] = useState(false);

    // create button disable 
    const [isDisabled, setIsDisabled] = useState(false);

    const [options, setOptions] = useState([]);   
    const [stations, setStations] = useState([]); 

    // for refresh use 
    const [forceDisabled, setForceDisabled] = useState(false);

    // init 
    const fetchData = async() => {
        setIsLoading(true)

        try {
            // clear out all the previous data 
            setResponses(null);

            const response = await RouteRootes.getRoutes(id);

            // if dont have data will reach 404 
            // data insert to 
            if(response.data._id) {
                setObjId(response.data._id);
            }

            setResponses(response.data);
            setForm(response.data);
        } catch (err) {
            if (err.response && err.response.status === 404) {
                navigateIfNotFound({err});
            }

            errorHandler({err, setErrors});
        } finally {
            setIsLoading(false);
        } 
    }

    const handleChange = (e) => {
        // get target name and values
        const {name, value} = e.target;

        setIsDisabled(false)

        if (name === "RouteId") {
            setFormErrors((prev) => ({
                ...prev,
                "RouteId" : "Route Id is unchangedable"
            }));
        }

        setForm((prev) => ({            
            ...prev,
            [name]: value, 
        }));
    }

    const handleUpdate = async(e) => {
        e.preventDefault();

        // loading start when access to database 
        setIsLoading(true);
        setErrors({});

        try {
            const response = await RouteRootes.updateRoutes(id, form);

            if (response.status === 200) {
                // success update 
                try {
                    const createRouteStation = {
                        RouteId : id,
                        StationList : stations  
                    }
                    const sencondResponse = await RouteStationRootes.modifyRoutesStations(createRouteStation)

                    if (sencondResponse.status === 200) {
                        
                        navigateIfSuccess({response});
                    }
                } catch (err) {
                    errorHandler({err, setErrors})
                }
                // no change will be redirect back to this page and display success message 
            } else if (response && response.error !== "") {
                // dont have create success, have some error
                const err = response.data.error; 
                setFormErrorsHandler({err, formErrors, setFormErrors});
            }
        } catch (err) {
            errorHandler({err, setErrors})
        } finally {
            setIsLoading(false);
        }
    }

    const handleDelete = async(e) => {
        e.preventDefault();

        // loading start when access to database 
        setIsLoading(true);
        setErrors({});

        try {
            const response = await RouteRootes.deleteRoutes(id);

            console.log(response)

            if (response.status === 200) {
                try {
                    const createRouteStation = {
                        RouteId : id,
                        StationList : []
                    }
                    const sencondResponse = await RouteStationRootes.modifyRoutesStations(createRouteStation)

                    if (sencondResponse.status === 200) {
                        
                        navigateIfSuccess({response});
                    }
                } catch (err) {
                    errorHandler({err, setErrors})
                }
            } 
        } catch (err) {
            errorHandler({err, setErrors})
        } finally {
            setIsLoading(false);
        }
    }

    useEffect(() => {
        // get data first 
        fetchData();
    }, []);

    return (
        <div>
            <Header 
                who={headerChoice.route}
            />
            <div style={{"height" : "600px", "marginTop" : "100px"}}>
                {isLoading ? (
                    <div className="w-100 h-100">
                        <Spinner />
                    </div>
                ) : Object.keys(errors).length > 0 ? (
                    <div className='ps-5 pe-5'>
                        <ErrorMessage err={errors} />
                    </div>
                ) : (
                    <div>
                        {successMessage && (
                            <div className='ps-5 pe-5'>
                                <SuccessMessage 
                                    message={successMessage}
                                />
                                {window.history.replaceState({}, '')} 
                            </div>
                        )}
                        <RouteForm 
                            setStations={setStations}
                            stations={stations}
                            setOptions={setOptions}
                            options={options}
                            isCreate={false}
                            form={form}
                            formErrors={formErrors}
                            handleChange={handleChange}
                            handleSubmit={handleUpdate}
                            handleDelete={handleDelete}
                            isDisabled={isDisabled}
                            forceDisaled={forceDisabled}
                        />
                    </div>
                )}
            </div>
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