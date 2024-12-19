import React from "react";
import { Route } from "react-router-dom";
import { staticRoutes, dynamicRoutes } from "../routes";
import { BusPage } from "../../pages/bus_page";
import { BusDetail } from "../../components/bus/bus_details";
import { BusCreate } from "../../components/bus/bus_create";

const BusRoutes = [
    <Route key="bus" path={staticRoutes.bus} element={<BusPage />} />,
    <Route key="bus-detail" path={staticRoutes.busDetail} element={<BusDetail />} />,
    <Route key="bus-create" path={staticRoutes.busCreate} element={<BusCreate />} />,
];

export default BusRoutes;