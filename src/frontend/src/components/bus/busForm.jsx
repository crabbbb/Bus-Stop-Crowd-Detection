import { CreateBtn, UpdateBtn, DeleteBtn } from "../shared/cudBtn";
import { Icontooltip } from "../shared/tooltips";
import { useNavigate } from "react-router-dom";
import { staticRoutes } from "../../routes/routes";

// change can be use for update and create but handleDelete is only for delete 
export function BusForm({isCreate, carplate = null, form, formErrors, handleSubmit, handleChange, handleDelete = null, isDisabled}) {
    const navigate = useNavigate();

    const handleBack = (e) => {
        e.preventDefault()

        navigate(staticRoutes.bus);
    }

    return (
        <div className='d-flex justify-content-center align-items-center fs-cus-1'>
            <form className='w-50 bg-light p-5 rounded-3 shadow-lg' onSubmit={handleSubmit}>
                <button type="button" class="btn p-0 mb-3 link-primary link-offset-2 link-opacity-50-hover" onClick={handleBack}>
                    <i class="bi bi-arrow-left-square-fill"></i> &nbsp; Back
                </button>
                {isCreate ? (
                    <h2 className='fw-bold'>Create New Bus</h2>
                ) : (
                    <h2 className='fw-bold'>Modify Bus {form.BusId} Detail</h2>
                )}
                {!isCreate ? (
                    // because is either delete or update so will have id 
                    <div>
                        <label class="form-label align-middle" for="disabledInput">Bus Id <Icontooltip icon={"bi-info-circle-fill"} content={"Unable to change Bus Id"}/> :</label>
                        <input class="form-control focus-ring focus-ring-danger" id="disabledInput" type="text" value={form.BusId} disabled/>
                    </div>
                ) : null}
                <div>
                    <label className="form-label mt-4 ms-1" for="CarPlateNo">Car Plate No. :</label>
                    <input type="text" value={form.CarPlateNo} className={`form-control ${formErrors.CarPlateNo ? "is-invalid" : ""}`} id="CarPlateNo" name="CarPlateNo" onChange={handleChange} placeholder="Eg, ABC1234" />
                    {/* info for similar pair */}
                    <div className="text-warning ms-1 mt-1">Similar Car Plate No : {carplate}</div>
                    <div className={`text-danger ms-1 mb-1 ${formErrors.CarPlateNo !== "" ? "" : "visually-hidden"}`}>{formErrors.CarPlateNo}</div>
                </div>
                <div>
                    <label className="form-label ms-1" for="inputValid">Capacity :</label>
                    <input type="number" className={`form-control fs-cus-1 ${formErrors.Capacity ? "is-invalid" : ""}`}  placeholder="Eg, 10" id="Capacity" name='Capacity' min={0} value={form.Capacity} onChange={handleChange} onKeyDown={(e) => {
                        if (e.key === "-") {
                            // prevent user type negative value
                            e.preventDefault();
                        }
                    }} />
                    <div className={`text-danger ms-1 mb-1 ${formErrors.Capacity !== "" ? "" : "visually-hidden"}`}>{formErrors.Capacity}</div>
                </div>
                <div>
                    <label for="IsActive" className="col-form-label ps-1">Bus Status :</label>
                    <select className="form-select fs-cus-1" id="IsActive" name='IsActive' value={form.IsActive} onChange={handleChange}>
                        <option value={0}>Active</option>
                        <option value={1}>NotActive</option>
                    </select>
                </div>
                {isCreate ? (
                    <div className='w-100 text-end mt-4'>
                        <CreateBtn 
                            isDisabled={isDisabled}
                        />
                    </div>
                ) : (
                    <div className='w-100 text-end mt-4'>
                        <UpdateBtn 
                            isDisabled={isDisabled}
                        />
                        &nbsp;&nbsp;&nbsp;
                        <DeleteBtn 
                            isDisabled={isDisabled}
                            handleDelete={handleDelete}
                        />
                    </div>
                )}
                
            </form>
        </div>
    )
}