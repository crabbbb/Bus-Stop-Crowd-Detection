import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import BusRootes from "../../routes/api/rootes/bus_rootes";

export function BusDetail() {
    // get the id from url 
    const {id} = useParams();

    // use to handle the data to be display 
    const [responses, setResponses] = useState({});
    // use to handle the error send back from backend 
    const [errors, setErrors] = useState([])

    const fetchData = async() => {
        try {
            // clear out all the previous data 
            setResponses(null);

            const response = await BusRootes.getBus(id);

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
        } 
    }

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div>
            Hello  World <br/>
            {responses && (
                <div>
                    <h2>Bus Information</h2>
                    {Object.keys(responses).map((key) => (
                        <p key={key}>
                            <strong>{key}:</strong> {responses[key]}
                        </p>
                    ))}
                </div>
            )}
        </div>
    );
}