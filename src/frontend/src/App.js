// import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './theme/customTheme.scss';
import 'jquery/dist/jquery.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'; // bootstrap Icon
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // bootstrap javascript 
import { HomePage } from './pages/homePage';
import { staticRoutes } from './routes/routes';
import BusRoutes from './routes/app/busRouter';
import RouteRoutes from './routes/app/routeRouter';
import ObjectDetection from './routes/app/objectDetectionRouter';
import React, { useState } from "react";
import Select from "react-select";

const NotFoundPage = () => <h1 className="center h-100 w-100 text-danger fw-bold">404 NOT FOUND!!</h1>

const DynamicDropdowns = () => {
  const options = [
    { value: "apple", label: "Apple" },
    { value: "banana", label: "Banana" },
    { value: "cherry", label: "Cherry" },
    { value: "date", label: "Date" },
    { value: "grape", label: "Grape" },
  ];

  const [dropdowns, setDropdowns] = useState([{ id: 1, selected: null }]);

  const addDropdown = () => {
    setDropdowns([...dropdowns, { id: dropdowns.length + 1, selected: null }]);
  };

  const handleChange = (selected, id) => {
    const updatedDropdowns = dropdowns.map((dropdown) =>
      dropdown.id === id ? { ...dropdown, selected } : dropdown
    );
    setDropdowns(updatedDropdowns);
    console.log(updatedDropdowns); // Logs all dropdown selections
  };

  return (
    <div>
      <h3>Dynamic Dropdowns</h3>
      {dropdowns.map((dropdown) => (
        <div key={dropdown.id} style={{ marginBottom: "10px" }}>
          <Select
            options={options}
            value={dropdown.selected}
            onChange={(selected) => handleChange(selected, dropdown.id)}
            placeholder="Search and select..."
          />
        </div>
      ))}
      <button onClick={addDropdown} style={{ marginTop: "10px" }}>
        Add Dropdown
      </button>
    </div>
  );
};

// export default DynamicDropdowns;



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
        {/* object detection */}
        {ObjectDetection}
      </Routes>
    </Router>
  );
}



export default App;
