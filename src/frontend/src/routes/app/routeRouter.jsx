import React from "react";
import { Route } from "react-router-dom";
import { staticRoutes, dynamicRoutes } from "../routes";
import { RoutePage } from "../../pages/routePage";
import { RouteCreate } from "../../components/route/routeCreate";
import { RouteDetail } from "../../components/route/routeDetail";

const RouteRoutes = [
    <Route key="route" path={staticRoutes.route} element={<RoutePage />} />,
    <Route key="route-create" path={staticRoutes.routeCreate} element={<RouteCreate />} />,
    <Route key="route-detail" path={staticRoutes.routeDetail} element={<RouteDetail />} />
];

export default RouteRoutes;