import React from "react";
import { Route } from "react-router-dom";
import { staticRoutes, dynamicRoutes } from "../routes";
import { BusPage } from "../../pages/busPage";
import { BusDetail } from "../../components/bus/busDetails";
import { BusCreate } from "../../components/bus/busCreate";

const BusRoutes = [
    <Route key="bus" path={staticRoutes.bus} element={<BusPage />} />,
    <Route key="bus-detail" path={staticRoutes.busDetail} element={<BusDetail />} />,
    <Route key="bus-create" path={staticRoutes.busCreate} element={<BusCreate />} />,
];

export default BusRoutes;