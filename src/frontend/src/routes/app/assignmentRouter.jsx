import React from "react";
import { Route } from "react-router-dom";
import { staticRoutes, dynamicRoutes } from "../routes";
import { AssignmentPage } from "../../pages/assignmentPage";
import { AssignmentCreate } from "../../components/assignment/assignmentCreate";
import { AssignmentDetail } from "../../components/assignment/assignmentDetail";

const AssignmentRouter = [
    <Route key="assignment" path={staticRoutes.assignment} element={<AssignmentPage />} />,
    <Route key="assignment-create" path={staticRoutes.assignmentCreate} element={<AssignmentCreate />} />,
    <Route key="assignment-detail" path={staticRoutes.assignmentDetail} element={<AssignmentDetail />} />,
];

export default AssignmentRouter;