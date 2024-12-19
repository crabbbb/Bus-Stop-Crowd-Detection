import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Header, headerChoice } from '../shared/header';
import { CreateBtn } from '../shared/cud_btn';
import BusRootes from '../../routes/api/rootes/bus_rootes';
import { Spinner } from '../shared/spinner';
import { ErrorMessage, SuccessMessage } from '../shared/display_message';
import { BusForm } from './bus_form';

export function BusCreate() {
    const navigate = useNavigate();

    const [carplate, setCarplate] = useState([])

    // handle form change
    const [form, setForm] = useState({ 
                                Capacity: "", 
                                CarPlateNo: "", 
                                IsActive: 0 
                            });
    
    // any error related to form 
    const [formErrors, setFormErrors] = useState({ 
                                            Capacity: "", 
                                            CarPlateNo: "", 
                                            IsActive: "" 
                                        });

    // use to handle the error which using 500 + / 400 + response 
    const [errors, setErrors] = useState(null);
    
    // spinner 
    const [isLoading, setIsLoading] = useState(false);

    // create button disable 
    const [isDisabled, setIsDisabled] = useState(false);

    const handleChange = (e) => {
        // get target name and values
        const {name, value} = e.target;

        let newValue;
        setIsDisabled(false)
        setFormErrors({ 
            Capacity: "", 
            CarPlateNo: "", 
            IsActive: "" 
        });

        // when is carplate changing update the current exist data 
        // if is exactly same with what list have, block the button 
        if (name === "CarPlateNo") {
            newValue = value.toUpperCase()

            if(value.length > 7) {
                setFormErrors((prev) => ({
                    ...prev,
                    CarPlateNo: "Car Plate Number cannot exceed 7 character"
                }));
                setIsDisabled(true)
            }

            // get the carplate 
            fetchCarPlateNo({"CarPlateNo" : value});
        } else {
            newValue = value
        }

        setForm((prevValues) => ({            
            ...prevValues,
            [name]: newValue, 
        }));
    }

    const fetchCarPlateNo = async(cp = {}) => {
        try {
            // clear all possible distrubted state
            setErrors(null);
            setCarplate("");

            const queryParams = new URLSearchParams(cp).toString();
            const response = await BusRootes.getCarPlate(queryParams);

            // get data and convert the format 
            const carplateList = response.data || [];

            // check data return 
            if (carplateList.length > 0) {
                // have similar carplate found 
                setCarplate(carplateList.map(item => item.CarPlateNo).join(", "));

                // check for exact match
                if (carplateList.some(item => item.CarPlateNo === cp.CarPlateNo)) {
                    // exact match found 
                    setFormErrors((prev) => ({
                        ...prev,
                        CarPlateNo: "Car Plate Number already exists"
                    }));

                    setIsDisabled(true)
                }
            } else {
                // no similar carplate found
                setCarplate("");
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

    const handleSubmit = async(e) => {
        e.preventDefault();
        try {
            const response = await BusRootes.createBus(form);

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
                who={headerChoice.bus}
            />
            <div style={{"height" : "600px", "marginTop" : "100px"}}> 
                {isLoading ? (
                    <Spinner />
                ) : errors ? (
                    <div className='ps-5 pe-5'>
                        <ErrorMessage err={errors} />
                    </div>
                ) : null}
                <BusForm
                    isCreate={true}
                    carplate={carplate}
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