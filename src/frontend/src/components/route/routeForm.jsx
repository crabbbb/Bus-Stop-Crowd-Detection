import { CreateBtn, UpdateBtn, DeleteBtn } from "../shared/cudBtn";
import { Icontooltip } from "../shared/tooltips";
import { useNavigate } from "react-router-dom";
import { staticRoutes } from "../../routes/routes";
import { DropdownWithInput } from "../shared/dropdown";

// change can be use for update and create but handleDelete is only for delete 
export function RouteForm({stations, setStations, setOptions, options, isCreate, form, formErrors, handleSubmit, handleChange, handleDelete = null, isDisabled, forceDisaled}) {
    const navigate = useNavigate();

    const handleBack = (e) => {
        e.preventDefault()

        navigate(staticRoutes.route);
    }

    return (
        <div className='d-flex justify-content-center align-items-center fs-cus-1'>
            <div className='w-50 bg-light p-5 rounded-3 shadow-lg'>
                <button type="button" class="btn p-0 mb-3 link-primary link-offset-2 link-opacity-50-hover" onClick={handleBack}>
                    <i class="bi bi-arrow-left-square-fill"></i> &nbsp; Back
                </button>
                {isCreate ? (
                    <h2 className='fw-bold'>Create New Routes</h2>
                ) : (
                    <h2 className='fw-bold'>Modify Route {form.RouteId} Detail</h2>
                )}
                {!isCreate ? (
                    // because is either delete or update so will have id 
                    <div>
                        <label class="form-label align-middle" for="disabledInput">Route Id <Icontooltip icon={"bi-info-circle-fill"} content={"Unable to change Route Id"}/> :</label>
                        <input class="form-control focus-ring focus-ring-danger" id="disabledInput" type="text" value={form.RouteId} disabled/>
                    </div>
                ) : null}
                <div>
                    <label className="form-label ms-1" for="RouteDuration">Route Duration (min) :</label>
                    <input type="number" className={`form-control fs-cus-1 ${formErrors.RouteDuration ? "is-invalid" : ""}`}  placeholder="Eg, 10" id="RouteDuration" name='RouteDuration' min={0} value={form.RouteDuration} onChange={handleChange} onKeyDown={(e) => {
                        if (e.key === "-" || e.key === ".") {
                            // prevent user type negative value
                            e.preventDefault();
                        }
                    }} />
                    <div className={`text-danger ms-1 mb-1 ${formErrors.RouteDuration !== "" ? "" : "visually-hidden"}`}>{formErrors.RouteDuration}</div>
                </div>
                <div>
                    <label className="col-form-label ps-1" for="FromCampus">From Campus <Icontooltip icon={"bi-info-circle-fill"} content={"First Station start at campus. Only routes marked From campus will carry passengers from the campus bus stop"}/> :</label>
                    <select className="form-select fs-cus-1" id="FromCampus" name='FromCampus' value={form.FromCampus} onChange={handleChange}>
                        <option value={0}>{"Yes"}</option>
                        <option value={1}>{"No"}</option>
                    </select>
                </div>
                <div>
                    <label for="IsActive" className="col-form-label ps-1">Bus Status :</label>
                    <select className="form-select fs-cus-1" id="IsActive" name='IsActive' value={form.IsActive} onChange={handleChange}>
                        <option value={0}>Active</option>
                        <option value={1}>NotActive</option>
                    </select>
                </div>
                <br/>
                <hr />
                <h4><b>Add Stopping Station</b></h4>
                <DropdownWithInput 
                    setOptions={setOptions}
                    options={options}
                    setStations={setStations}
                    stations={stations}
                />
                {isCreate ? (
                    <div className='w-100 text-end mt-4'>
                        <CreateBtn 
                            isDisabled={isDisabled}
                            handleSubmit={handleSubmit}
                        />
                    </div>
                ) : (
                    <div className='w-100 text-end mt-4'>
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
                
            </div>
        </div>
    )
}