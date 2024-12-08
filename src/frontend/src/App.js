import React, { useEffect, useState } from "react";
import axios from "axios";

const BusData = () => {
  const [busData, setBusData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch data from the Django backend
    axios
      .get("http://127.0.0.1:8000/api/bus-data/") // Adjust the URL if needed
      .then((response) => {
        setBusData(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Bus Data</h1>
      <table border="1">
        <thead>
          <tr>
            <th>ID</th>
            <th>Route</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {busData.map((bus) => (
            <tr key={bus.id}>
              <td>{bus.id}</td>
              <td>{bus.route}</td>
              <td>{bus.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BusData;
