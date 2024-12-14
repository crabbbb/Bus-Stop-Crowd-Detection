import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './theme/custom_theme.scss';
import 'jquery/dist/jquery.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'; // bootstrap Icon
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // bootstrap javascript 
import { HomePage } from './pages/home_page';
import { staticRoutes } from './routes/routes';
import BusRoutes from './routes/app/bus_router';

const NotFoundPage = () => <h1 className="center">404 NOT FOUND!!</h1>

function Timer() {
  // State for tracking values of the two input boxes
  const [values, setValues] = useState({
      input1: "",
      input2: "",
  });

  // Generalized handler function for input changes
  const handleChange = (e) => {
      const { name, value } = e.target;
      setValues((prevValues) => ({
          ...prevValues,
          [name]: value, // Update only the specific field
      }));
  };

  return (
      <div style={{ textAlign: "center", margin: "auto" }}>
          <h1 style={{ color: "Green" }}>GeeksforGeeks</h1>
          <h3>Example for React Input Boxes and Updates</h3>
          
          {/* First Input Box */}
          <div>
              <label htmlFor="input1">Input Box 1:</label>
              <input
                  type="text"
                  name="input1"
                  id="input1"
                  value={values.input1}
                  onChange={handleChange}
                  style={{ margin: "10px" }}
              />
          </div>
          
          {/* Second Input Box */}
          <div>
              <label htmlFor="input2">Input Box 2:</label>
              <input
                  type="text"
                  name="input2"
                  id="input2"
                  value={values.input2}
                  onChange={handleChange}
                  style={{ margin: "10px" }}
              />
          </div>
          
          <br />
          {/* Displaying updated values */}
          <div>
              <strong>User Inputs:</strong>
              <p>Input 1: {values.input1}</p>
              <p>Input 2: {values.input2}</p>
          </div>
      </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path={staticRoutes.home} element={<HomePage />} />
        {/* others */}
        <Route path="/test" element={<Timer />} />
        <Route path="*" element={<NotFoundPage />} />
        {/* bus */}
        {BusRoutes}
      </Routes>
    </Router>
  );
}

export default App;
