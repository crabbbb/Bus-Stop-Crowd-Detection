import React, { useEffect, useState } from 'react';
import routes from '../routes';
import BusDisplay from '../components/bus/bus_display';

export function BusPage() {
    return (
        <div className="d-flex justify-content-center align-items-center" style={{height: 500 + 'px'}}>
            <div className="h-50">
                <h1 className="text-center">BUS</h1>
                <a href='/bus/display'>Click Me</a>
            </div>
        </div>
    )
}
