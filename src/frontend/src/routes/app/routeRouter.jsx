import React from "react";
import { Route } from "react-router-dom";
import { staticRoutes, dynamicRoutes } from "../routes";
import { RoutePage } from "../../pages/routePage";
import { RouteCreate } from "../../components/route/routeCreate";

const RouteRoutes = [
    <Route key="route" path={staticRoutes.route} element={<RoutePage />} />,
    <Route key="route" path={staticRoutes.routeCreate} element={<RouteCreate />} />,
];

export default RouteRoutes;