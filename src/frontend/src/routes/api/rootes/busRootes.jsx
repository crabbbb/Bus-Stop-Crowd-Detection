import bus_schedule from "../busSchedule";

const BusRootes = {
    getBuss: (data) => bus_schedule.get(`/bus?${data}`),
    getBus: (id) => bus_schedule.get(`/bus/${id}/`),
    createBus: (bus) => bus_schedule.post("/bus/", bus),
    updateBus: (id, bus) => bus_schedule.put(`/bus/${id}/`, bus),
    deleteBus: (id) => bus_schedule.delete(`/bus/${id}/`),
    getCarPlate: (carplate) => bus_schedule.get(`/carplate?${carplate}`)
};

export default BusRootes;