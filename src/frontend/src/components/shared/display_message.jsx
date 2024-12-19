export function InfoMessage({message}) {
    return (
        <div class="alert alert-dismissible alert-info mt-4 fs-cus-1">
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            {message}
        </div>
    );
}

export function SuccessMessage({message}) {
    return (
        <div class="alert alert-dismissible alert-success mt-4 fs-cus-1">
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            {message}
        </div>
    );
}

export function ErrorMessage({err}) {
    return (
        <div class="alert alert-dismissible alert-danger mt-4 fs-cus-1">
            <h4 class="alert-heading">Error !</h4>
            <ul>
                {Object.keys(err).map((key) => {
                    if (err[key] != "") {
                        return (<li key={key}>
                            {key} : {err[key]}
                        </li>)
                    }
                })}
            </ul>
        </div>
    );
}