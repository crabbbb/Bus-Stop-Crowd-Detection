import bus_schedule from "../busSchedule";

const AssignmentRootes = {
    getAssignments: (data) => bus_schedule.get(`/assignment?${data}`),
    getAssignment: (id) => bus_schedule.get(`/assignment/${id}/`),
    createAssignment: (assignment) => bus_schedule.post("/assignment/", assignment),
    updateAssignment: (id, assignment) => bus_schedule.put(`/assignment/${id}/`, assignment),
    deleteAssignment: (id) => bus_schedule.delete(`/assignment/${id}/`),
};

export default AssignmentRootes;