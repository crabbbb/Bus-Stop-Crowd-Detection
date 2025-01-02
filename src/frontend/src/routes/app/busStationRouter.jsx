import React from "react";
import { Route } from "react-router-dom";
import { staticRoutes, dynamicRoutes } from "../routes";
import { BusStationPage } from "../../pages/busStationPage";
import { BusStationCreate } from "../../components/busStation/busStationCreate";
import { BusStationDetail } from "../../components/busStation/busStationDetail";

const BusStationRouter = [
    <Route key="busStation" path={staticRoutes.busStation} element={<BusStationPage />} />,
    <Route key="busStation-create" path={staticRoutes.busStationCreate} element={<BusStationCreate />} />,
    <Route key="busStation-detail" path={staticRoutes.busStationDetail} element={<BusStationDetail />} />,
];

export default BusStationRouter;