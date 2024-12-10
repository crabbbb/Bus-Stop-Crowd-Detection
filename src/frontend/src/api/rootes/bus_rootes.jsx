import bus_schedule from "../bus_schedule";

const BusRootes = {
    getBuss: (data) => {
        const queryParams = new URLSearchParams(data).toString();
        bus_schedule.get(`/busSchedule/bus?${queryParams}`)
    },
    getBus: (id) => bus_schedule.get(`/busSchedule/bus/${id}`),
    createBus: (data) => bus_schedule.post("/busSchedule/bus/", data),
    updateBus: (id, data) => bus_schedule.put(`/busSchedule/bus/${id}`, data),
    deleteBus: (id) => bus_schedule.delete(`/busSchedule/bus/${id}`),
};

export default BusRootes;