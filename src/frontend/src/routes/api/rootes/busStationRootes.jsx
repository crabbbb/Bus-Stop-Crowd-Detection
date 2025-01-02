import bus_schedule from "../busSchedule";

const BusStationRootes = {
    getBusStations: (data) => bus_schedule.get(`/busStation?${data}`),
    getBusStation: (id) => bus_schedule.get(`/busStation/${id}/`),
    createBusStation: (busStation) => bus_schedule.post("/busStation/", busStation),
    updateBusStation: (id, busStation) => bus_schedule.put(`/busStation/${id}/`, busStation),
    deleteBusStation: (id) => bus_schedule.delete(`/busStation/${id}/`),
    getStationName: (stationName) => bus_schedule.get(`/stationName?${stationName}`) 
};

export default BusStationRootes;