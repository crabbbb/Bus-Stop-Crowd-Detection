import bus_schedule from "../busSchedule";

const RouteRootes = {
    getRoutess: (data) => bus_schedule.get(`/route?${data}`),
    getRoutes: (id) => bus_schedule.get(`/route/${id}/`),
    createRoutes: (route) => bus_schedule.post("/route/", route),
    updateRoutes: (id, route) => bus_schedule.put(`/route/${id}/`, route),
    deleteRoutes: (id) => bus_schedule.delete(`/route/${id}/`),
};

export default RouteRootes;