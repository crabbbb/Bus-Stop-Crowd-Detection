import axios from "axios";

const bus_schedule = axios.create({
    baseURL: "http://127.0.0.1:8000/busSchedule", 
});

export default bus_schedule;