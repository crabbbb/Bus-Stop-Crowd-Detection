import { CreateBtn, UpdateBtn, DeleteBtn } from "../shared/cudBtn";
import { Icontooltip } from "../shared/tooltips";
import { useNavigate } from "react-router-dom";
import { staticRoutes } from "../../routes/routes";
import BusRootes from "../../routes/api/rootes/busRootes";
import RouteStation from "../../routes/api/rootes/routeStationRootes";
import { useEffect, useState } from "react";
import Select from "react-select";

// This is your child form component
export function AssignmentForm({ isCreate, setForm, form, formErrors, handleSubmit, handleChange, handleDelete = null, isDisabled, forceDisaled }) {
    const navigate = useNavigate();
    const [busIdOptions, setBusIdOptions] = useState([]);
    const [routeIdOptions, setRouteIdOptions] = useState([]);

    // Fetch data from the backend using useEffect
    useEffect(() => {
        const fetchData = async () => {
        try {
            // 1) Bus list
            const response = await BusRootes.getBuss();
            // Suppose response.data is an array like: [{ BusId: 'B001', CarPlateNo: 'ABC123' }, ...]
            const fetchedData = response.data;
            const formattedOptions = fetchedData.map((item) => ({
            value: item.BusId,
            label: item.BusId + " > " + item.CarPlateNo
            }));
            setBusIdOptions(formattedOptions);
        } catch (error) {
            console.error("Error fetching bus data:", error);
        }

        try {
            // 2) Routes + station order
            const response2 = await RouteStation.getRouteWithStations();
            // If your backend returns { data: [ {RouteId, StationOrder}, ... ] }
            // then you must do "response2.data.data"
            // or if your backend directly returns the array, do "response2.data"
            const fetchedData2 = response2.data.data; 
            // e.g. [ { RouteId: 'R006', StationOrder: 'Station 1 > East Campus' }, ... ]

            const formattedOptions2 = fetchedData2.map((item) => ({
            value: item.RouteId,
            label: item.RouteId + " > " + item.StationOrder
            }));
            setRouteIdOptions(formattedOptions2);
        } catch (error) {
            console.error("Error fetching route data:", error);
        }
        };

        fetchData();
    }, []);

    // onChange for the bus Select
    const handleBusChange = (selected) => {
        // selected is { value: 'B001', label: 'B001 > ABC123' }
        setForm((prev) => ({
        ...prev,
        BusId: selected
        }));
    };

    // onChange for the route Select
    const handleRouteChange = (selected) => {
        setForm((prev) => ({
        ...prev,
        RouteId: selected
        }));
    };

    const handleBack = (e) => {
        e.preventDefault();
        navigate(staticRoutes.assignment);
    };

    return (
        <div className="d-flex justify-content-center align-items-center fs-cus-1">
        <form className="w-50 bg-light p-5 rounded-3 shadow-lg">
            <button type="button" className="btn p-0 mb-3 link-primary link-offset-2 link-opacity-50-hover" onClick={handleBack}>
                <i className="bi bi-arrow-left-square-fill"></i> &nbsp; Back
            </button>

            {isCreate ? (
                <h2 className="fw-bold">Create New Assignment</h2>
            ) : (
                <h2 className="fw-bold">Modify Assignment {form.AssignmentId} Detail</h2>
            )}

            {/* If not create, show assignmentId field... */}
            {!isCreate && (
                <div>
                    <label className="form-label align-middle" htmlFor="disabledInput">
                        Assignment Id &nbsp; <Icontooltip icon={"bi-info-circle-fill"} content={"Unable to change Assignment Id"} /> :
                    </label>
                    <input className="form-control focus-ring focus-ring-danger" id="disabledInput" type="text" value={form.AssignmentId} disabled/>
                </div>
            )}

            {/* Time field */}
            <div>
            <label className="form-label mt-4 ms-1" htmlFor="Time"> Time : </label>
            <input
                id="Time"
                name="Time"
                type="time"
                value={form.Time?.substring(0, 5)} 
                // e.g. if form.Time is "08:00:00", substring(0,5) => "08:00"
                onChange={handleChange}
                className={`form-control ${formErrors.Time ? "is-invalid" : ""}`}
            />
            {formErrors.Time && <div className="text-danger">{formErrors.Time}</div>}
            </div>

            {/* DayOfWeek field */}
            <div>
            <label className="form-label mt-2 ms-1" htmlFor="DayOfWeek">
                Day Of Week :
            </label>
            <select
                className="form-select fs-cus-1"
                id="DayOfWeek"
                name="DayOfWeek"
                value={form.DayOfWeek}
                onChange={handleChange}
            >
                <option value={1}>MONDAY</option>
                <option value={2}>TUESDAY</option>
                <option value={3}>WEDNESDAY</option>
                <option value={4}>THURSDAY</option>
                <option value={5}>FRIDAY</option>
                <option value={6}>SATURDAY</option>
                <option value={0}>SUNDAY</option>
            </select>
            {formErrors.DayOfWeek && <div className="text-danger">{formErrors.DayOfWeek}</div>}
            </div>

            {/* BusId (React-Select) */}
            <div>
                <label htmlFor="BusId" className="col-form-label ps-1 mt-2">
                    Bus Id :
                </label>
                <Select
                    options={busIdOptions}
                    value={form.BusId}
                    onChange={handleBusChange}
                    placeholder="Select an option"
                    isLoading={busIdOptions.length === 0}
                />
                {formErrors.BusId && <div className="mt-4 text-danger">{formErrors.BusId}</div>}
            </div>

            {/* RouteId (React-Select) */}
            <div>
                <label htmlFor="RouteId" className="col-form-label ps-1">
                    Route Id :
                </label>
                <Select
                    options={routeIdOptions}
                    value={form.RouteId}
                    onChange={handleRouteChange}
                    placeholder="Select an option"
                    isLoading={routeIdOptions.length === 0}
                />
                {formErrors.RouteId && <div className="text-danger">{formErrors.RouteId}</div>}
            </div>

            {/* Buttons */}
            {isCreate ? (
            <div className="w-100 text-end mt-4">
                <CreateBtn isDisabled={isDisabled} handleSubmit={handleSubmit} />
            </div>
            ) : (
            <div className="w-100 text-end mt-4">
                <UpdateBtn
                isDisabled={forceDisaled ? true : isDisabled ? true : false}
                handleSubmit={handleSubmit}
                />
                &nbsp;&nbsp;&nbsp;
                <DeleteBtn
                isDisabled={forceDisaled ? true : isDisabled ? true : false}
                handleDelete={handleDelete}
                />
            </div>
            )}
        </form>
        </div>
    );
}
