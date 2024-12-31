import React, { useState, useEffect } from 'react';
import { Spinner } from '../components/shared/spinner';
import { Header, headerChoice } from '../components/shared/header';

export function VideoStream() {
    const [imageSrc, setImageSrc] = useState(null);
    const [numPeople, setNumPeople] = useState(null);
    const [busData, setBusData] = useState({});
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        let eventSource;

        const connectToStream = () => {
            eventSource = new EventSource('http://127.0.0.1:8000/objectDetection/stream/');

            eventSource.onmessage = (event) => {
                try {
                    // Parse the JSON data
                    const parsedData = JSON.parse(event.data);
                    // "frame", "num_people", "busCentroid"
                    setImageSrc(`data:image/jpeg;base64,${parsedData.frame}`);
                    setNumPeople(parsedData.num_people);
                    setBusData(parsedData.busCentroid);
                    setIsLoading(false);

                    
                } catch (error) {
                    console.error('Failed to parse SSE data:', error);
                }
            };

            eventSource.onerror = (err) => {
                console.error('EventSource failed:', err);
                eventSource.close();

                // retry sending the request every 3 seconds if error
                setTimeout(() => {
                    console.log('Retrying connection...');
                    connectToStream();
                }, 3000); 
            };
        };

        connectToStream();

        return () => {
            if (eventSource) {
                eventSource.close();
            }
        };
    }, []);

    return (
        <div>
            <Header 
                who={headerChoice.objectDetection}
            />
            <div className='p-5' style={{"marginTop" : "70px"}}>
                {isLoading ? (
                    <Spinner />
                ) : (
                    <div>
                        <h2 className='ps-5 pb-2'>Bus Stop Crowd Detection</h2>
                        <div className='d-flex justify-content-center row'>
                            <div className='col-2' style={{ width: "70%"}}>
                                {imageSrc && <img src={imageSrc} alt="Video Stream" className="rounded-start rounded-3 border border-primary shadow" style={{ width: "100%"}}/>}
                            </div>
                            <div className='bg-secondary col-1 rounded-3 p-4' style={{ width: "25%"}}>
                                <div>
                                    {/* for other information */}
                                    <p className='fs-cus-1'>Number of person in queue : <span className={``}>{numPeople ?? 'N/A'}</span></p>
                                </div>
                                <hr/>
                                <div>
                                    {/* for bus stop 4 */}
                                    <h5>Station 4</h5>
                                    <ul>
                                        <li></li>
                                    </ul>
                                </div>
                                <hr/>
                                <div>
                                    {/* for bus stop 5 */}
                                    <h5>Station 5</h5>
                                </div>
                                <p>Number of people detected: {numPeople ?? 'N/A'}</p>
                        
                                <pre>{JSON.stringify(busData, null, 2)}</pre> {/* For debugging */}
                            </div>
                        </div>
                    </div>
                )}        
            </div>
            
        </div>
    );
}

export default VideoStream;
