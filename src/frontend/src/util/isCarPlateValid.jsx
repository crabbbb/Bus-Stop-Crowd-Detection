import BusRootes from "../routes/api/rootes/busRootes";

export function isCarPlateValid({setFormErrors, formErrors, setIsDisabled, setErrors, setCarplate, value = ""}) {
    
    if(value.length > 7) {
        setFormErrors((prev) => ({
            ...prev,
            CarPlateNo: "Car Plate Number cannot exceed 7 character"
        }));
        setIsDisabled(true)
    }

    // get the carplate 
    fetchCarPlateNo({"CarPlateNo" : value.toUpperCase()}, setErrors, setCarplate, setFormErrors, formErrors, setIsDisabled);
}

const fetchCarPlateNo = async(cp = {}, setErrors, setCarplate, setFormErrors, formErrors, setIsDisabled) => {
    try {
        // clear all possible distrubted state
        setErrors({});
        setCarplate("");

        const queryParams = new URLSearchParams(cp).toString();
        
        const response = await BusRootes.getCarPlate(queryParams);

        // get data and convert the format 
        const carplateList = response.data || [];

        // check data return 
        if (carplateList.length > 0) {
            // have similar carplate found 
            setCarplate(carplateList.map(item => item.CarPlateNo).join(", "));

            // ensure dont overwrite the error message 
            if (formErrors.CarPlateNo === "") { 
                // check for exact match
                if (carplateList.some(item => item.CarPlateNo === cp.CarPlateNo)) {
                    // exact match found 
                    setFormErrors((prev) => ({
                        ...prev,
                        CarPlateNo: "Car Plate Number already exists"
                    }));

                    setIsDisabled(true);
                }
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
