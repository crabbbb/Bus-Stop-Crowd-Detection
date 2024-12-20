// import React, { useEffect, useState } from "react";

// const WebSocketTest = () => {
//   const [messages, setMessages] = useState([]);
//   let socket;

//   useEffect(() => {
//     // Open WebSocket connection
//     socket = new WebSocket("ws://127.0.0.1:8000/ws/test/");

//     socket.onopen = () => {
//       console.log("WebSocket connected");
//     };

//     socket.onmessage = (event) => {
//       // Handle server messages
//       const data = JSON.parse(event.data);
//       setMessages((prevMessages) => [...prevMessages, data.response]);
//     };

//     socket.onclose = () => {
//       console.log("WebSocket disconnected");
//     };

//     return () => socket.close(); // Cleanup on component unmount
//   }, []);

//   const sendMessage = () => {
//     if (socket && socket.readyState === WebSocket.OPEN) {
//       socket.send(JSON.stringify({ message: "Hello, Server!" }));
//     }
//   };

//   return (
//     <div>
//       <h1>WebSocket Test</h1>
//       <button onClick={sendMessage}>Send Message</button>
//       <ul>
//         {messages.map((msg, index) => (
//           <li key={index}>{msg}</li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default WebSocketTest;

import React, { useEffect, useState } from "react";

const DatabaseUpdateStream = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const eventSource = new EventSource("http://127.0.0.1:8000/busSchedule/database-update-stream/");

    eventSource.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data]);
    };

    eventSource.onerror = (error) => {
      console.error("EventSource error:", error);
      eventSource.close(); // Close the connection if there's an error
    };

    return () => eventSource.close();
  }, []);

  return (
    <div>
      <h1>Database Updates</h1>
      <ul>
        {messages.map((msg, index) => (
          <li key={index}>{msg}</li>
        ))}
      </ul>
    </div>
  );
};

export default DatabaseUpdateStream;
