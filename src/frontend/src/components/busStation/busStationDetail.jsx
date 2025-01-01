import React, { useEffect, useState } from 'react';
import { Header, headerChoice } from '../shared/header';
import { useParams, useLocation } from "react-router-dom";
import { UseNavigateIfSuccess, UseNavigateIfNotFound } from "../../util/navigatePage";
import { Spinner } from '../shared/spinner';
import { ErrorMessage } from '../shared/displayMessage';
import { BusStationForm } from './busStationForm';
import BusStationRootes from '../../routes/api/rootes/busStationRootes';
import { errorHandler, setFormErrorsHandler } from "../../util/errorHandler";

export function BusStationDetail() {
    // get the id from url 
    const {id} = useParams();
    console.log(id)

    // use to get the success 
    const location = useLocation();
    let { successMessage } = location.state || {};

    const navigateIfSuccess = UseNavigateIfSuccess();
    const navigateIfNotFound = UseNavigateIfNotFound();

    const [stationName, setStationName] = useState([])

    const [objId, setObjId] = useState("");

    const [responses, setResponses] = useState({});

    // handle form change
    const [form, setForm] = useState({ 
                                StationId: "",
                                StationName: ""
                            });
    
    // any error related to form 
    const [formErrors, setFormErrors] = useState({ 
                                            StationId: "",
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

    const fetchStationName = async(stationName) => {
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

    // init 
    const fetchData = async() => {
        setIsLoading(true)

        try {
            // clear out all the previous data 
            setResponses(null);

            const response = await BusStationRootes.getBusStation(id);

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
        setFormErrors({ 
            StationId: "",
            StationName: ""
        });

        if (name === "StationId") {
            setFormErrors((prev) => ({
                ...prev,
                "StationId" : "Station Id is unchangedable"
            }));
        }

        if (name === "StationName") {
            fetchStationName({"StationName" : value})
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
            const response = await BusStationRootes.updateBusStation(id, form);

            if (response.status === 200) {
                // success update 
                navigateIfSuccess({response});
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
            const response = await BusStationRootes.deleteBusStation(id);

            if (response.status === 200) {
                navigateIfSuccess({response});
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
                    isCreate={false}
                    stationName={stationName}
                    form={form}
                    formErrors={formErrors}
                    handleChange={handleChange}
                    handleSubmit={handleUpdate}
                    handleDelete={handleDelete}
                    isDisabled={isDisabled}
                    forceDisaled={forceDisabled}
                />
            </div>
        </div>
    )
}