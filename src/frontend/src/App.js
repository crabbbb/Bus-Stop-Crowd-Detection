import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './theme/custom_theme.scss';
import 'bootstrap-icons/font/bootstrap-icons.css'; // bootstrap Icon
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // bootstrap javascript 
import {RedirectBtn} from './components/shared/redirect_btn';
import {HomePage} from './pages/home_page';
import routes from './routes';
import {BusPage} from './pages/bus_page';
import {BusDisplay} from './components/bus/bus_display';
import {Header} from './components/shared/header';

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
      <Header />
      <Routes>
        <Route path={routes.home} element={<HomePage />} />
        <Route path={routes.bus} element={<BusPage />} />
        <Route path="/bus/display" element={<BusDisplay />} />
        <Route path="/test" element={<Timer />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
}

export default App;
