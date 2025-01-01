import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Header, headerChoice } from '../shared/header';
import BusRootes from '../../routes/api/rootes/busRootes';
import { Spinner } from '../shared/spinner';
import { ErrorMessage } from '../shared/displayMessage';
import { BusStationForm } from './busStationForm';
import BusStationRootes from '../../routes/api/rootes/busStationRootes';
import { errorHandler, setFormErrorsHandler } from "../../util/errorHandler";

export function BusStationCreate() {
    const navigate = useNavigate();

    const [stationName, setStationName] = useState([])

    // handle form change
    const [form, setForm] = useState({ 
                                StationName: ""
                            });
    
    // any error related to form 
    const [formErrors, setFormErrors] = useState({ 
                                            StationName: ""
                                        });

    // use to handle the error which using 500 + / 400 + response 
    const [errors, setErrors] = useState({});
    
    // spinner 
    const [isLoading, setIsLoading] = useState(false);

    // create button disable 
    const [isDisabled, setIsDisabled] = useState(false);

    // for refresh use 
    const [forceDisabled, setForceDisabled] = useState(false);

    const fetchStationName = async(stationName = {}) => {
        try {
            // clear all possible distrubted state
            setErrors({});
            setStationName("");
    
            const queryParams = new URLSearchParams(stationName).toString();
            
            const response = await BusStationRootes.getStationName(queryParams);
    
            // get data and convert the format 
            const stationNameList = response.data || [];
    
            // check data return 
            if (stationNameList.length > 0) {
                // have similar carplate found 
                setStationName(stationNameList.map(item => item.StationName).join(", "));
    
                // ensure dont overwrite the error message 
                if (formErrors.StationName === "") { 
                    // check for exact match
                    console.log(stationName)
                    if (stationNameList.some(item => item.StationName === stationName.StationName)) {
                        // exact match found 
                        setFormErrors((prev) => ({
                            ...prev,
                            StationName: "Station name already exists"
                        }));
                        setIsDisabled(true);
                    }
                }
            } else {
                // no similar carplate found
                setStationName("");
            }
        } catch (err) {
            errorHandler({err, setErrors})
        } 
    }

    const handleChange = (e) => {
        // get target name and values
        const {name, value} = e.target;

        setIsDisabled(false)
        setFormErrors({ 
            StationName: ""
        });

        if (name === "StationName") {
            fetchStationName({"StationName" : value})
        }

        setForm((prev) => ({            
            ...prev,
            [name]: value, 
        }));
    }

    const handleSubmit = async(e) => {
        e.preventDefault();
        try {
            const response = await BusStationRootes.createBusStation(form);

            if (response.status === 201) {
                // create success 
                const message = response.data.success;
                const redirect = response.data.redirect;

                console.log(message)

                navigate(redirect, {state: {successMessage: message}});
            }

            if (response && response.error !== "") {
                console.log(response)
                // dont have create success, have some error 
                Object.keys(response.data.error).map((key) => {
                    if (formErrors.hasOwnProperty(key)) {
                        setFormErrors((prev) => ({
                            ...prev,
                            [key]: response.data.error[key] || "Unknown error", 
                        }));
                    }
                })
            }
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
        }
    }
    
    return (
        <div>
            <Header 
                who={headerChoice.busStation}
            />
            <div style={{"height" : "600px", "marginTop" : "100px"}}> 
                {isLoading ? (
                    <Spinner />
                ) : Object.keys(errors).length > 0 ? (
                    <div className='ps-5 pe-5'>
                        <ErrorMessage err={errors} />
                    </div>
                ) : null}
                <BusStationForm
                    isCreate={true}
                    stationName={stationName}
                    form={form}
                    formErrors={formErrors}
                    handleSubmit={handleSubmit}
                    handleChange={handleChange}
                    isDisabled={isDisabled}
                />
            </div>
        </div>
    )
}