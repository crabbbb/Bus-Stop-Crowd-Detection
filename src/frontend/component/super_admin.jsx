import React from 'react';
import routes from '../routes';

export default function SuperAdminRedirect() {
    
    const handleRedirect = () => {
        window.location.href = routes.superadmin; // Django default admin URL
    };

    return (
        <p onClick={handleRedirect} className="text-end m-4 text-decoration-underline">
            Superuser ?
        </p>
    );
}