import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './theme/custom_theme.scss';
import 'jquery/dist/jquery.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'; // bootstrap Icon
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // bootstrap javascript 
import { HomePage } from './pages/home_page';
import { staticRoutes } from './routes/routes';
import BusRoutes from './routes/app/bus_router';

const NotFoundPage = () => <h1 className="center h-100 w-100 text-danger fw-bold">404 NOT FOUND!!</h1>

function App() {
  return (
    <Router>
      <Routes>
        <Route path={staticRoutes.home} element={<HomePage />} />
        {/* others */}
        <Route path="*" element={<NotFoundPage />} />
        {/* bus */}
        {BusRoutes}
      </Routes>
    </Router>
  );
}

export default App;
