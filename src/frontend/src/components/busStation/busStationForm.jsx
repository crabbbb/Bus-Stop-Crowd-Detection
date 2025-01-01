import { CreateBtn, UpdateBtn, DeleteBtn } from "../shared/cudBtn";
import { Icontooltip } from "../shared/tooltips";
import { useNavigate } from "react-router-dom";
import { staticRoutes } from "../../routes/routes";

// change can be use for update and create but handleDelete is only for delete 
export function BusStationForm({isCreate, stationName, form, formErrors, handleSubmit, handleChange, handleDelete, isDisabled, forceDisaled}) {
    const navigate = useNavigate();

    const handleBack = (e) => {
        e.preventDefault()

        navigate(staticRoutes.busStation);
    }

    return (
        <div className='d-flex justify-content-center align-items-center fs-cus-1'>
            <form className='w-50 bg-light p-5 rounded-3 shadow-lg'>
                <button type="button" class="btn p-0 mb-3 link-primary link-offset-2 link-opacity-50-hover" onClick={handleBack}>
                    <i class="bi bi-arrow-left-square-fill"></i> &nbsp; Back
                </button>
                {isCreate ? (
                    <h2 className='fw-bold'>Create New Bus Station</h2>
                ) : (
                    <h2 className='fw-bold'>Modify Bus Station {form.StationId} Detail</h2>
                )}
                {!isCreate ? (
                    // because is either delete or update so will have id 
                    <div>
                        <label class="form-label align-middle" for="disabledInput">Station Id <Icontooltip icon={"bi-info-circle-fill"} content={"Unable to change Bus Id"}/> :</label>
                        <input class="form-control focus-ring focus-ring-danger" id="disabledInput" type="text" value={form.StationId} disabled/>
                    </div>
                ) : null}
                <div>
                    <label className="form-label mt-4 ms-1" for="StationName">Station Name :</label>
                    <input type="text" value={form.StationName} className={`form-control ${formErrors.StationName ? "is-invalid" : ""}`} id="StationName" name="StationName" onChange={handleChange} placeholder="Eg, MRT ABC" />
                    {/* info for similar pair */}
                    <div className="text-warning ms-1 mt-1">Similar Station Name : {stationName}</div>
                    <div className={`text-danger ms-1 mb-1 ${formErrors.StationName !== "" ? "" : "visually-hidden"}`}>{formErrors.StationName}</div>
                </div>
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
            </form>
        </div>
    )
}