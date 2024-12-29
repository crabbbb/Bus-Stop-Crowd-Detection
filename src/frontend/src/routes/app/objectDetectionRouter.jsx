import { VideoStream } from "../../pages/videoStream";
import { staticRoutes } from "../routes";
import { Route } from "react-router-dom";

const ObjectDetection = [
    <Route key="videoStream" path={staticRoutes.objectDetection} element={<VideoStream />} />,
];

export default ObjectDetection;