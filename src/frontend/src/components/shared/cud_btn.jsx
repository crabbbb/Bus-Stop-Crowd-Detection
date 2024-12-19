
export function CreateBtn({isDisabled}) {
    return (
        <button type="submit" className={`btn ${isDisabled ? "btn-grey" : "btn-success"}`} disabled={isDisabled}>Create</button>
    )
}