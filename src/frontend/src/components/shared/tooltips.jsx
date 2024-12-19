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
        <button ref={tooltipRef} className="btn d-inline p-0 text-info-emphasis" style={{"font-size" : "12px"}}>
            <i className={`"bi ${icon} text-secondary"`}></i>
        </button>
    )
}