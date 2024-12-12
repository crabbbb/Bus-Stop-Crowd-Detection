import React from "react";
import { Route } from "react-router-dom";
import { staticRoutes, dynamicRoutes } from "../routes";
import { BusPage } from "../../pages/bus_page";
import { BusDisplay } from "../../components/bus/bus_display";
import { BusDetail } from "../../components/bus/bus_details";

const BusRoutes = [
    <Route key="bus" path={staticRoutes.bus} element={<BusPage />} />,
    <Route key="bus-display" path="/bus/display" element={<BusDisplay />} />,
    <Route key="bus-detail" path={staticRoutes.busDetail} element={<BusDetail />} />,
];

export default BusRoutes;