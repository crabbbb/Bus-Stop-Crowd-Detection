// react page link ( not for backend request )
const staticRoutes = {
    home: "/",
    notfound: "*",
    bus: "/bus",
    busCreate: "/bus/create",
    busDetail: "/bus/detail/:id", // static for router configuration
    route: "/route",
    routeCreate: "/route/create",
    routeDetail: "/route/detail/:id",
    busStation: "/busStation",
    busStationCreate: "/busStation/create",
    busStationDetail: "/busStation/detail/:id",
    objectDetection: "/objectDetection", 
};

// dynamic required to pass in some value 
const dynamicRoutes = {
    detail: (where, id) => `/${where}/detail/${id}`, 
}

export { staticRoutes, dynamicRoutes };