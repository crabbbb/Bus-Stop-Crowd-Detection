import React, { useEffect, useState } from 'react';
import BusRootes from '../../api/rootes/bus_rootes';
import bus_schedule from '../../api/bus_schedule';
import axios from 'axios';

export function BusDisplay() {
    // use to handle the data to be display 
    const [responses, setResponses] = useState([]);
    // use to handle the data user fill in in filter 
    const [filters, setFilters] = useState({ 
                                        BusId: "", 
                                        Capacity: "", 
                                        CarPlateNo: "", 
                                        IsActive: "" 
                                    });
    // use to handle the error send back from backend 
    const [errors, setErrors] = useState([])
    const [filterErrors, setFilterErrors] = useState({ 
                                                BusId: "", 
                                                Capacity: "", 
                                                CarPlateNo: "", 
                                                IsActive: "" 
                                            });
    
    // create function for fetching data from backend 
    const fetchData = async (params = {}) => {
        try {
            // clear out all the previous data 
            setResponses(null)
            setErrors(null)

            // send together with filter 
            const response = await BusRootes.getBuss({params});

            // set response to responses
            setResponses(response.data);

            console.log(response.data)
        } catch (err) {
            // store err in error
            if (err.response) {
                setErrors(`Error ${err.response.status}: ${err.response.statusText}`);
            } else if (err.request) {
                setErrors("No response from the server. Please try again later.");
            } else {
                setErrors("An unexpected error occurred.");
            }
        }
    };

    // onchange update 
    const handleChange = (e) => {
        // get target name and values 
        const {name, value} = e.target;

        // ignore other 
        // prevValues = current state / the data that currently store inside the filter 
        // [name]: value is current data 
        // ...prevValues = the other data that not include the target name 
        // ensure the data will be update but at the sametime wont remove the old value 
        setFilters((prevValues) => ({            
            ...prevValues,
            [name]: value, 
        }));
    };

    // submit btn
    const handleSubmit = () => {
        fetchData(filters);
    };

    // initial fecthing when page load
    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div className='p-4'>
            {/* filter input */}
            <form className='bg-sur-container p-4 rounded-top'>
                <legend className='text-primary cus-font'><b>BUS MANAGEMENT</b></legend>
                <div className='row'>
                    {/* bus id - text */}
                    <div className='col'>
                        <label class="col-form-label ps-1" for="BusId">Bus Id :</label>
                        <input type="text" className="form-control fs-cus-1" placeholder="Filter By Bus Id" id="BusId" name="BusId" value={filters.BusId} onChange={handleChange} />
                    </div>
                    {/* capacity */}
                    <div className='col'>
                        <label class="col-form-label ps-1" for="Capacity">Bus Capacity <span class="badge bg-warning">(Must greater than 0)</span> : </label>
                        <input type="number" class="form-control fs-cus-1" placeholder="Filter By Bus Capacity" id="Capacity" name='Capacity' min={0} value={filters.Capacity} onChange={handleChange} onKeyDown={(e) => {
                            if (e.key === "-") {
                                // prevent user type negative value
                                e.preventDefault();
                            }
                        }} />
                    </div>
                </div>
                <div className='row'>
                    {/* carplate - text */}
                    <div className='col'>
                        <label class="col-form-label ps-1" for="CarPlateNo">Car Plate No. :</label>
                        <input type="text" class="form-control fs-cus-1" placeholder="Filter By Car Plate No" id="CarPlateNo" name='CarPlateNo' value={filters.CarPlateNo} onChange={handleChange} />
                    </div>
                    {/* is active - checklist */}
                    <div className='col'>
                        <label for="IsActive" class="col-form-label ps-1">Bus Status :</label>
                        <select class="form-select fs-cus-1" id="IsActive" name='IsActive' value={filters.IsActive} onChange={handleChange}>
                            <option>-</option>
                            <option>Active</option>
                            <option>Not Active</option>
                        </select>
                    </div>
                </div>
                <div className='row text-end d-flex justify-content-end mt-4'>
                    <div className='w-25'>
                        <button type="button" class="btn btn-info fs-cus-1 w-50 me-3 rounded-pill">Filter</button>
                    </div>
                </div>
            </form>
            
            
            {/* Table Display
            <table>
                <thead>
                <tr>
                    <th>Bus ID</th>
                    <th>Capacity</th>
                    <th>Car Plate No</th>
                    <th>Is Active</th>
                </tr>
                </thead>
                <tbody>
                {data.map((item) => (
                    <tr key={item.BusId}>
                    <td>{item.BusId}</td>
                    <td>{item.Capacity}</td>
                    <td>{item.CarPlateNo}</td>
                    <td>{item.IsActive ? "✅" : "❌"}</td>
                    </tr>
                ))}
                </tbody>
            </table> */}
            </div>
        );
}