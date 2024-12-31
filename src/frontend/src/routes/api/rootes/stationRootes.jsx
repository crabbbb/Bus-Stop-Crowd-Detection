import bus_schedule from "../busSchedule";

const BusStation = {
    getStations: (data) => bus_schedule.get(`/busStation?${data}`),
    getStation: (id) => bus_schedule.get(`/busStation/${id}/`),
    createStation: (busStation) => bus_schedule.post("/busStation/", busStation),
    updateStation: (id, busStation) => bus_schedule.put(`/busStation/${id}/`, busStation),
    deleteStation: (id) => bus_schedule.delete(`/busStation/${id}/`),
};

export default BusStation;