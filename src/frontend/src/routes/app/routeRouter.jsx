import React from "react";
import { Route } from "react-router-dom";
import { staticRoutes, dynamicRoutes } from "../routes";
import { RoutePage } from "../../pages/routePage";

const RouteRoutes = [
    <Route key="route" path={staticRoutes.route} element={<RoutePage />} />,
];

export default RouteRoutes;