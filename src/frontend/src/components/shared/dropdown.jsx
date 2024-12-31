import { useState, useEffect } from "react";
import Select from "react-select";
import BusStation from "../../routes/api/rootes/stationRootes";

export function DropdownWithInput({setOptions, options, stations, setStations}) {
    // const [options, setOptions] = useState([]);   
    // const [stations, setStations] = useState([]); 

    useEffect(() => {
        BusStation
        .getStations()
            .then((res) => {
                const data = res.data;
                // data might look like: 
                // [ { id: 101, stationName: 'Station A' }, { id: 102, stationName: 'Station B' }, ... ]
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