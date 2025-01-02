import { useState, useEffect } from "react";
import Select from "react-select";
import BusStation from "../../routes/api/rootes/stationRootes";
import RouteStation from "../../routes/api/rootes/routeStationRootes";

export function DropdownWithInput({setOptions, options, stations, setStations}) {
    useEffect(() => {
        BusStation
        .getStations()
            .then((res) => {
                const data = res.data;
                // data might look like: 
                // [ { id: 'Station A', stationName: 'Station A' }, { id: 102, stationName: 'Station B' }, ... ]
                const dropdownOptions = data.map((station) => ({
                    value: station.StationName,
                    label: station.StationName,
                }));
                setOptions(dropdownOptions);
            })
            .catch((err) => console.error('Error fetching options:', err));
    }, []);
    

    const handleSelectChange = (selectedOption, index) => {
        const updatedStations = [...stations];
        updatedStations[index].id = selectedOption.value;
        updatedStations[index].stationName = selectedOption.label;
        setStations(updatedStations);
    };
    
    // add
    const handleAddStation = () => {
        const newStation = {
            id: null,
            stationName: '',
            order: stations.length + 1,
        };
        setStations((prev) => [...prev, newStation]);
    };
    
    // remove 
    const handleRemoveStation = (index) => {
        const updatedStations = [...stations];
        updatedStations.splice(index, 1);

        // Re-sequence the order
        const reordered = updatedStations.map((station, i) => ({
            ...station,
            order: i + 1,
        }));
        setStations(reordered);
    };

    return (
        <div className="w-100">
            {stations.map((station, index) => (
                <div key={index} style={{ display: 'flex', alignItems: 'center', marginBottom: '10px'}} className="mt-3" >
                    <div style={{ marginRight: '10px', width: "100px"}}>Order {station.order}:</div><br/>
                    <Select
                        options={options}
                        value={
                            station.id ? { value: station.id, label: station.stationName } : null
                        }
                        onChange={(selectedOption) => handleSelectChange(selectedOption, index)}
                        placeholder="Select a station"
                        className='form-control p-0'
                    />
                    {/* Remove button */}
                    <button onClick={() => handleRemoveStation(index)} style={{ marginLeft: '10px' }} className="btn btn-danger text-light"> <i class="bi bi-x-circle-fill"></i></button>
                </div>
            ))}
            <div className="w-100 text-end p-0 m-0 mt-4">
                {/* Add station button */}
                <button onClick={handleAddStation} className="btn btn-success bg-primary text-light"> <i class="bi bi-plus-circle-fill"></i> Add Station</button>
            </div>
        </div>
    );
};

export function DropdownWithInputValueReady({ routeId, setOptions, options, stations, setStations }) {
    
    useEffect(() => {
        // Fetch the existing stations for this route
        RouteStation.getRoutesStations(routeId)
            .then((res) => {
            // Example response: 
            // [ { RouteId: 'R001', StationName: 'MRT', RouteOrder: 1 }, { RouteId: 'R001', StationName: 'ABC', RouteOrder: 2 }, ... ]
            const data = res.data;
            console.log("Route Station response:", res.data);
    
            // Sort by RouteOrder so they display in the correct sequence
            const sortedData = data.sort((a, b) => { return parseInt(a.RouteOrder) - parseInt(b.RouteOrder)});
    
            // Convert them into our local station structure
            // e.g. { id: 'MRT', stationName: 'MRT', order: 1 }
            const mappedStations = sortedData.map((item) => ({
                id: item.StationName,           
                stationName: item.StationName,
                order: item.RouteOrder,
            }));
    
            setStations(mappedStations);
            })
            .catch((err) => console.error('Error fetching route stations:', err));
    
        // Fetch all possible stations for the dropdown
        BusStation.getStations()
            .then((res) => {
            // Example response:
            // [ { StationName: 'MRT', IsActive: 0 }, { StationName: 'ABC', IsActive: 1 }, ... ]
            const data = res.data;
    
            // Map them into { value, label } for react-select
            const dropdownOptions = data.map((station) => ({
                value: station.StationName,
                label: station.StationName,
            }));
    
            setOptions(dropdownOptions);
            })
            .catch((err) => console.error('Error fetching stations:', err));
        }, [routeId]);
    
        // ---------------------------------
        // Handle user changing a dropdown selection
        // ---------------------------------
        const handleSelectChange = (selectedOption, index) => {
        const updatedStations = [...stations];
        updatedStations[index].id = selectedOption.value;
        updatedStations[index].stationName = selectedOption.label;
        setStations(updatedStations);
        };
    
        // ---------------------------------
        // Add a new (blank) station
        // ---------------------------------
        const handleAddStation = () => {
        // Next order is length + 1
        const newStation = {
            id: null,
            stationName: '',
            order: stations.length + 1,
        };
        setStations((prev) => [...prev, newStation]);
        };
    
        // ---------------------------------
        // Remove a station
        // ---------------------------------
        const handleRemoveStation = (index) => {
        const updatedStations = [...stations];
        updatedStations.splice(index, 1);
    
        // Recalculate order
        const reordered = updatedStations.map((station, i) => ({
            ...station,
            order: i + 1,
        }));
        setStations(reordered);
        };
    
        return (
            <div className="w-100">
                {stations.map((station, index) => (
                <div
                    key={index}
                    style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}
                    className="mt-3"
                >
                    <div style={{ marginRight: '10px', width: "100px" }}>
                    Order {station.order}:
                    </div>
        
                    <Select
                    // React-Select options
                    options={options}
                    // The current value: ensure it matches { value, label }
                    value={
                        station.id 
                        ? { value: station.id, label: station.stationName }
                        : null
                    }
                    onChange={(selectedOption) => handleSelectChange(selectedOption, index)}
                    placeholder="Select a station"
                    className="form-control p-0"
                    />
        
                    {/* Remove button */}
                    <button
                    onClick={() => handleRemoveStation(index)}
                    style={{ marginLeft: '10px' }}
                    className="btn btn-danger text-light"
                    >
                    <i className="bi bi-x-circle-fill"></i>
                    </button>
                </div>
                ))}
        
                <div className="w-100 text-end p-0 m-0 mt-4">
                {/* Add station button */}
                <button
                    onClick={handleAddStation}
                    className="btn btn-success bg-primary text-light"
                >
                    <i className="bi bi-plus-circle-fill"></i> Add Station
                </button>
                </div>
            </div>
        );
}
