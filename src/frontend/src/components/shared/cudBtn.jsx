
export function CreateBtn({isDisabled, handleSubmit}) {
    return (
        <button type="submit" className={`btn ${isDisabled ? "btn-grey" : "btn-success"}`} disabled={isDisabled} onClick={handleSubmit}>Create</button>
    )
}

export function UpdateBtn({isDisabled, handleSubmit}) {
    return (
        <button className={`btn ${isDisabled ? "btn-grey" : "bg-orange"}`} disabled={isDisabled} onClick={handleSubmit}>Update</button>
    )
}

export function DeleteBtn({isDisabled, handleDelete}) {
    return (
        <button className={`btn ${isDisabled ? "btn-grey" : "bg-danger"}`} disabled={isDisabled} onClick={handleDelete}>Delete</button>
    )
}