import React from "react";
import { RedirectBtn } from "../components/shared/redirect_btn";
import { staticRoutes } from "../routes/routes";
import { SuperAdminRedirect } from "../components/super_admin";
import { Header, headerChoice } from "../components/shared/header";

export function HomePage() {
    return (
        <div>
            <Header
                who={headerChoice.home}
            />
            <div className="d-flex justify-content-center align-items-center" style={{height: 500 + 'px'}}>
                <div className="h-50">
                    <h1 className="text-center">Welcome USER! &#128512;</h1>
                    <div className="d-flex justify-content-center align-items-center h-75">
                        <RedirectBtn
                            redirectTo={staticRoutes.bus}
                            btnContent="OBJECT DETECTION"
                            btnClass="btn btn-secondary m-4 w-50 h-75 cus-font"
                        />
                        <RedirectBtn
                            redirectTo={staticRoutes.bus}
                            btnContent="BUS SCHEDULE MANAGEMENT"
                            btnClass="btn btn-secondary m-4 w-50 h-75 cus-font"
                        />
                    </div>
                    <SuperAdminRedirect />
                </div>
            </div>
        </div>
    )
}
