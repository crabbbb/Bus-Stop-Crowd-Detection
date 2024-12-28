import React, { useState, useEffect } from "react";
import { useParams, useLocation } from "react-router-dom";
import { UseNavigateIfSuccess, UseNavigateIfNotFound } from "../../util/navigatePage";
import { Header, headerChoice } from "../shared/header";
import { BusForm } from "./busForm";
import { Spinner } from "../shared/spinner";
import { SuccessMessage, ErrorMessage } from "../shared/displayMessage";
import { isCarPlateValid } from "../../util/isCarPlateValid";
import { errorHandler, setFormErrorsHandler } from "../../util/errorHandler";
import BusRootes from "../../routes/api/rootes/busRootes";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export function BusDetail() {
    // get the id from url 
    const {id} = useParams();
    
    // use to get the success 
    const location = useLocation();
    let { successMessage } = location.state || {};

    const navigateIfSuccess = UseNavigateIfSuccess();
    const navigateIfNotFound = UseNavigateIfNotFound();

    const [carplate, setCarplate] = useState([])

    // use to handle the data to be display from backend to frontend, init value 
    const [responses, setResponses] = useState({});

    const [objId, setObjId] = useState("");
    
    // fdrm is for handle the change in the form 
    const [form, setForm] = useState({ 
                                        BusId: "",
                                        Capacity: "", 
                                        CarPlateNo: "", 
                                        IsActive: 0 
                                    });

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

    // for refresh use 
    const [forceDisabled, setForceDisabled] = useState(false);


    // Create refs to store the latest values
    const responsesRef = React.useRef(responses);
    const formRef = React.useRef(form);
    const objIdRef = React.useRef(objId);

    // Keep refs in sync with state
    useEffect(() => {
        responsesRef.current = responses;
    }, [responses]);

    useEffect(() => {
        formRef.current = form;
    }, [form]);

    useEffect(() => {
        objIdRef.current = objId;
    }, [objId]);
        
    // init 
    const fetchData = async() => {
        setIsLoading(true)

        try {
            // clear out all the previous data 
            setResponses(null);

            const response = await BusRootes.getBus(id);

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

        let newValue;
        setIsDisabled(false)
        setFormErrors({ 
            Capacity: "", 
            CarPlateNo: "", 
            IsActive: "" 
        });

        if (name === "BusId") {
            setFormErrors((prev) => ({
                ...prev,
                "BusId" : "Bus Id is unchangedable"
            }));

            newValue = id;
        } else if (name === "CarPlateNo") {
            // when is carplate changing update the current exist data 
            // if is exactly same with what list have, block the button 
            newValue = value.toUpperCase()

            if (newValue !== responses.CarPlateNo) {
                isCarPlateValid({setFormErrors, formErrors, setIsDisabled, setErrors, setCarplate, value}); 
            }
        } else {
            newValue = value
        }

        setForm((prev) => ({            
            ...prev,
            [name]: newValue, 
        }));
    }

    const handleUpdate = async(e) => {
        e.preventDefault();

        // loading start when access to database 
        setIsLoading(true);
        setErrors({});

        try {
            const response = await BusRootes.updateBus(id, form);

            if (response.status === 200) {
                // success update 
                // no change will be redirect back to this page and display success message 
                navigateIfSuccess({response});
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
            const response = await BusRootes.deleteBus(id);

            console.log(response)

            if (response.status === 200) {
                // success update 
                // no change will be redirect back to this page and display success message 
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

    useEffect(() => {
        const eventSource = new EventSource("http://127.0.0.1:8000/busSchedule/busMonitor/");

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const operationType = data.operationType;
            let fullDocument = data.fullDocument;
            
            if (operationType === "delete") {
                fullDocument = data.documentKey;
            }

            // compare the id pass in and the current id 
            if (objIdRef.current === fullDocument._id) {    
                // is same, do some action 
                setForceDisabled(true);
                // pop notification 
                if (operationType === "delete") {
                    toast.error("Bus Id " + formRef.current.BusId + " have been deleted !");
                } else {
                    toast.warning("Bus Id " + formRef.current.BusId + " record have been changed ! Please refresh to get the latest value");
                }
            }
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
                        <BusForm 
                            isCreate={false}
                            carplate={carplate}
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