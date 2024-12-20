
export function CreateBtn({isDisabled}) {
    return (
        <button type="submit" className={`btn ${isDisabled ? "btn-grey" : "btn-success"}`} disabled={isDisabled}>Create</button>
    )
}

export function UpdateBtn({isDisabled}) {
    return (
        <button type="submit" className={`btn ${isDisabled ? "btn-grey" : "bg-orange"}`} disabled={isDisabled}>Update</button>
    )
}

export function DeleteBtn({isDisabled, handleDelete}) {
    return (
        <button className={`btn ${isDisabled ? "btn-grey" : "bg-danger"}`} disabled={isDisabled} onClick={handleDelete}>Delete</button>
    )
}