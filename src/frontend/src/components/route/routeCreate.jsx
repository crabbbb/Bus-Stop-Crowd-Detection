import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Header, headerChoice } from '../shared/header';
import { Spinner } from '../shared/spinner';
import { ErrorMessage } from '../shared/displayMessage';
import { RouteForm } from './routeForm';
import RouteRootes from '../../routes/api/rootes/routeRootes';
import RouteStationRootes from '../../routes/api/rootes/routeStationRootes';
import { errorHandler } from '../../util/errorHandler';

export function RouteCreate() {
    const navigate = useNavigate();

    // handle form change
    const [form, setForm] = useState({ 
                                RouteDuration: "", 
                                FromCampus: 0, 
                                IsActive: 0 
                            });
    
    // any error related to form 
    const [formErrors, setFormErrors] = useState({ 
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

    const handleChange = (e) => {
        // get target name and values
        const {name, value} = e.target;

        setIsDisabled(false)
        setFormErrors({ 
            RouteDuration: "", 
            FromCampus: "", 
            IsActive: "" 
        });

        setForm((prev) => ({            
            ...prev,
            [name]: value, 
        }));
    }

    const handleSubmit = async(e) => {
        e.preventDefault();
        try {
            const response = await RouteRootes.createRoutes(form)

            if (response.status === 201) {
                // create success 
                const message = response.data.success;
                const redirect = response.data.redirect;
                const id = response.data.id

                // start the Station
                const createRouteStation = {
                    RouteId : id,
                    StationList : stations  
                }
                const secondResponse = await RouteStationRootes.modifyRoutesStations(createRouteStation)

                if (secondResponse.status === 200) {
                    navigate(redirect, {state: {successMessage: message}});
                }
            }

            if (response && response.error !== "") {
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
            errorHandler({err, setErrors})
        }
    }
    
    return (
        <div>
            <Header 
                who={headerChoice.route}
            />
            <div style={{"height" : "600px", "marginTop" : "100px"}}> 
                {isLoading ? (
                    <Spinner />
                ) : Object.keys(errors).length > 0 ? (
                    <div className='ps-5 pe-5'>
                        <ErrorMessage err={errors} />
                    </div>
                ) : null}
                <RouteForm
                    setStations={setStations}
                    stations={stations}
                    setOptions={setOptions}
                    options={options}
                    isCreate={true}
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