// react page link ( not for backend request )
const staticRoutes = {
    home: "/",
    schedule: "/schedule",
    bus: "/bus",
    busCreate: "/bus/create",
    busDetail: "/bus/detail/:id", // static for router configuration
    route : "/route",
    superadmin: "http://127.0.0.1:8000/admin/",
};

// dynamic required to pass in some value 
const dynamicRoutes = {
    detail: (where, id) => `/${where}/detail/${id}`, 
}

export { staticRoutes, dynamicRoutes };