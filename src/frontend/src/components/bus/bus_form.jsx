import { CreateBtn, UpdateBtn } from "../shared/cud_btn";
import { Icontooltip } from "../shared/tooltips";


export function BusForm({isCreate, data = null, carplate, form, formErrors, handleSubmit, handleChange, isDisabled}) {
    // ensure data also have data
    if (data === null) {
        data = form;
    }

    return (
        <div className='d-flex justify-content-center align-items-center fs-cus-1'>
            <form className='w-50 bg-light p-5 rounded-3 shadow-lg' onSubmit={handleSubmit}>
                {isCreate ? (
                    <h2 className='fw-bold'>Create New Bus</h2>
                ) : (
                    <h2 className='fw-bold'>Modify Bus {data.BusId} Detail</h2>
                )}
                {!isCreate ? (
                    // because is either delete or update so will have id 
                    <div>
                        <label class="form-label align-middle" for="disabledInput">Bus Id <Icontooltip icon={"bi-info-circle-fill"} content={"Unable to change Bus Id"}/> :</label>
                        <input class="form-control" id="disabledInput" type="text" value={data.BusId} disabled/>
                    </div>
                ) : null}
                <div>
                    <label className="form-label mt-4 ms-1" for="CarPlateNo">Car Plate No. :</label>
                    <input type="text" value={form.CarPlateNo} className={`form-control ${formErrors.CarPlateNo ? "is-invalid" : ""}`} id="CarPlateNo" name="CarPlateNo" onChange={handleChange} placeholder="Eg, ABC1234" />
                    {/* info for similar pair */}
                    <div className="text-warning ms-1 mt-1">Similar Car Plate No : {carplate}</div>
                    <div className={`text-danger ms-1 mb-1 ${formErrors.CarPlateNo != "" ? "" : "visually-hidden"}`}>{formErrors.CarPlateNo}</div>
                </div>
                <div>
                    <label className="form-label ms-1" for="inputValid">Capacity :</label>
                    <input type="number" className={`form-control fs-cus-1 ${formErrors.Capacity ? "is-invalid" : ""}`}  placeholder="Eg, 10" id="Capacity" name='Capacity' min={0} value={form.Capacity} onChange={handleChange} onKeyDown={(e) => {
                        if (e.key === "-") {
                            // prevent user type negative value
                            e.preventDefault();
                        }
                    }} />
                    <div className={`text-danger ms-1 mb-1 ${formErrors.Capacity != "" ? "" : "visually-hidden"}`}>{formErrors.Capacity}</div>
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
                        <div>
                            <UpdateBtn 
                                isDisabled={isDisabled}
                            />
                        </div>
                        <div>
                            <UpdateBtn 
                                isDisabled={isDisabled}
                            />
                        </div>
                    </div>
                )}
                
            </form>
        </div>
    )
}