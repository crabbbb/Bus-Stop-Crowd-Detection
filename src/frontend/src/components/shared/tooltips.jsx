import { useRef, useEffect } from "react";
import { Tooltip } from "bootstrap/dist/js/bootstrap.bundle.min";

export function Icontooltip({icon, content}) {
    const tooltipRef = useRef(); 
    
    useEffect(() => {
        var tooltip = new Tooltip(tooltipRef.current, {
            title: content,
            placement: 'right',
            trigger: 'hover'
        })
    })

    return (
        <div ref={tooltipRef} className="btn d-inline p-0 text-info-emphasis" style={{"fontsize" : "12px"}} >
            <i className={`"bi ${icon} text-secondary"`}></i>
        </div>
    )
}