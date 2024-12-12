import bus_schedule from "../bus_schedule";

const BusRootes = {
    getBuss: (data) => bus_schedule.get(`/bus?${data}`),
    getBus: (id) => bus_schedule.get(`/bus/${id}`),
    createBus: (data) => bus_schedule.post("/bus/", data),
    updateBus: (id, data) => bus_schedule.put(`/bus/${id}`, data),
    deleteBus: (id) => bus_schedule.delete(`/bus/${id}`),
};

export default BusRootes;