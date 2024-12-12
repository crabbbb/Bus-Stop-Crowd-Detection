import React from 'react';
import { staticRoutes } from '../routes/routes';

export function SuperAdminRedirect() {
    
    const handleRedirect = () => {
        window.location.href = staticRoutes.superadmin; // Django default admin URL
    };

    return (
        <p onClick={handleRedirect} className="text-end m-4 text-decoration-underline">
            Superuser ?
        </p>
    );
}
