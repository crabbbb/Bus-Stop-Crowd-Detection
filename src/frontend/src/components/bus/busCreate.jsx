import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Header, headerChoice } from '../shared/header';
import BusRootes from '../../routes/api/rootes/busRootes';
import { Spinner } from '../shared/spinner';
import { ErrorMessage } from '../shared/displayMessage';
import { BusForm } from './busForm';
import { isCarPlateValid } from '../../util/isCarPlateValid';

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
    const [errors, setErrors] = useState({});
    
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

            isCarPlateValid({setFormErrors, formErrors, setIsDisabled, setErrors, setCarplate, value});
        } else {
            newValue = value
        }

        setForm((prev) => ({            
            ...prev,
            [name]: newValue, 
        }));
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
                ) : Object.keys(errors).length > 0 ? (
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