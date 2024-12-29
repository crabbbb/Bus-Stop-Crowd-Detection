import React, { useState, useEffect } from 'react';

export function VideoStream() {
    const [imageSrc, setImageSrc] = useState(null);
    const [numPeople, setNumPeople] = useState(null);
    const [busData, setBusData] = useState({});

    useEffect(() => {
        const eventSource = new EventSource('http://127.0.0.1:8000/objectDetection/stream/');

        eventSource.onmessage = (event) => {
        try {
            // Parse the JSON data
            const parsedData = JSON.parse(event.data);
            // "frame", "num_people", "busCentroid"
            setImageSrc(`data:image/jpeg;base64,${parsedData.frame}`);
            setNumPeople(parsedData.num_people);
            setBusData(parsedData.busCentroid);
        } catch (error) {
            console.error('Failed to parse SSE data:', error);
        }
        };

        eventSource.onerror = (err) => {
        console.error('EventSource failed:', err);
        eventSource.close();
        };

        return () => {
        eventSource.close();
        };
    }, []);

    return (
        <div>
        <h2>Real-time Video Stream</h2>
        <p>Number of people detected: {numPeople ?? 'N/A'}</p>
        {imageSrc && <img src={imageSrc} alt="Video Stream" style={{ width: '640px' }} />}
        <pre>{JSON.stringify(busData, null, 2)}</pre> {/* For debugging */}
        </div>
    );
}

export default VideoStream;
