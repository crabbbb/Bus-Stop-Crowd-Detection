import bus_schedule from "../busSchedule";

const RouteStation = {
    getRoutesStations: (id) => bus_schedule.get(`/routeStation/${id}/`),
    modifyRoutesStations: (routeStation) => bus_schedule.post("/routeStation/", routeStation),
    getRouteWithStations: () => bus_schedule.get(`/routeWithStation/`),
};

export default RouteStation;