import bus_schedule from "../busSchedule";

const RouteStation = {
    getRoutesStations: (id) => bus_schedule.get(`/routeStation/${id}/`),
    modifyRoutesStations: (routeStation) => bus_schedule.post("/routeStation/", routeStation),
};

export default RouteStation;