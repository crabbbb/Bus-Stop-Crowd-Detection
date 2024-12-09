import React, { useEffect, useState } from 'react';
import BusRootes from '../../api/rootes/bus_rootes';
import axios from 'axios';
import bus_schedule from '../../api/bus_schedule';

export default function BusDisplay() {
    // for display in table 
    const [data, setData] = useState([]);
    const [filters, setFilters] = useState({ BusId: "", Capacity: "", CarPlateNo: "", IsActive: "" });
    
    useEffect(() => {
        const fetchData = async () => {
            try{
                // const response = await axios.get('http://127.0.0.1:8000/busSchedule/bus/');
                const response = await BusRootes.buss(filters);
                setData(response.data);
                console.log(response.data)
            } catch (error) {
                console.error("Error happen when during fetching data : ", error)
            }
        };

        fetchData();

    }, [filters]);

    // Handle filter change
    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilters({ ...filters, [name]: value }); // Update filters
    };

    return (
        <div>
            <h1>Data Table</h1>
                
            <form>
            <div>
                <label>Bus ID:</label>
                <input
                    type="text"
                    name="BusId"
                    value={filters.BusId}
                    onChange={handleFilterChange}
                    placeholder="Filter by Bus ID"
                />
            </div>
            <div>
                <label>Capacity:</label>
                <input
                    type="text"
                    name="Capacity"
                    value={filters.Capacity}
                    onChange={handleFilterChange}
                    placeholder="Filter by Capacity"
                />
            </div>
            <div>
                <label>Car Plate No:</label>
                <input
                    type="text"
                    name="CarPlateNo"
                    value={filters.CarPlateNo}
                    onChange={handleFilterChange}
                    placeholder="Filter by Car Plate No"
                />
            </div>
            <div>
                <label>Is Active:</label>
                <input
                    type="text"
                    name="IsActive"
                    value={filters.IsActive}
                    onChange={handleFilterChange}
                    placeholder="Filter by Is Active"
                />
            </div>
        </form>

            
            {/* Table Display */}
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
            </table>
            </div>
        );
}
