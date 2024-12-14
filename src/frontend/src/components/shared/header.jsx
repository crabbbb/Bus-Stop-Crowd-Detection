import React from "react";
import { staticRoutes } from "../../routes/routes";

export function Header(who) {
    const active = "active fw-semibold text-decoration-underline text-primary";

    return (
        <nav class="navbar navbar-expand-lg bg-header header-font" data-bs-theme="light">
        <div class="container-fluid">
            <a class="navbar-brand text-primary fs-logo" href={staticRoutes.home}><b>BSCD</b></a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarColor03" aria-controls="navbarColor03" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarColor03">
                <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a className={`nav-link ${active ? who == headerChoice.home : ""}`} href={staticRoutes.home}>{headerChoice.home}</a>
                </li>
                <li class="nav-item">
                    <a className={`nav-link ${active ? who == headerChoice.test : ""}`} href="/test">{headerChoice.test}</a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Bus Schedule Management</a>
                    <div class="dropdown-menu bg-header">
                        <a className={`dropdown-item ${active ? who == headerChoice.bus : ""}`} href={staticRoutes.bus}>{headerChoice.bus}</a>
                        <a className={`dropdown-item ${active ? who == headerChoice.route : ""}`} href={staticRoutes.route}>{headerChoice.route}</a>
                    </div>
                </li>
                </ul>
            </div>
            </div>
        </nav>
    );
};

export const headerChoice = {
    test : "Test",
    home : "Home", 
    bus : "Bus",
    station : "Station",
    route : "Route",
}

