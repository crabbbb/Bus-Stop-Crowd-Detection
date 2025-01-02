import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './theme/customTheme.scss';
import 'jquery/dist/jquery.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'; // bootstrap Icon
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // bootstrap javascript 
import { HomePage } from './pages/homePage';
import { staticRoutes } from './routes/routes';
import BusRoutes from './routes/app/busRouter';
import RouteRoutes from './routes/app/routeRouter';
import BusStationRouter from './routes/app/busStationRouter';
import ObjectDetection from './routes/app/objectDetectionRouter';
import React from "react";
import AssignmentRouter from './routes/app/assignmentRouter';

const NotFoundPage = () => <h1 className="center h-100 w-100 text-danger fw-bold text-center">404 NOT FOUND!!</h1>

function App() {
  return (
    <Router>
      <Routes>
        <Route path={staticRoutes.home} element={<HomePage />} />
        {/* others */}
        <Route path={staticRoutes.notfound} element={<NotFoundPage />} />
        {/* bus */}
        {BusRoutes}
        {/* routes */}
        {RouteRoutes}
        {/* bus station */}
        {BusStationRouter}
        {/* assignment */}
        {AssignmentRouter}
        {/* object detection */}
        {ObjectDetection}
      </Routes>
    </Router>
  );
}



export default App;
