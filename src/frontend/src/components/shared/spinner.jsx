export function Spinner() {
    return (
        <div
            className="w-100 text-center row align-items-center justify-content-center p-5"
            style={{ height: "30px" }}
        >
            <div class="spinner-grow text-primary me-2" role="status">
            <span class="visually-hidden">Loading...</span>
            </div>
            <div class="spinner-grow text-success me-2" role="status">
            <span class="visually-hidden">Loading...</span>
            </div>
            <div class="spinner-grow text-secondary me-2" role="status">
            <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    );
}
