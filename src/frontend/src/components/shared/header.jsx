import React from "react";
import { staticRoutes } from "../../routes/routes";

export function Header() {
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
                    <a class="nav-link active fw-semibold text-decoration-underline rounded text-primary" href={staticRoutes.home}>Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/test">Test</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Pricing</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">About</a>
                </li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Dropdown</a>
                    <div class="dropdown-menu bg-header">
                    <a class="dropdown-item" href="#">Action</a>
                    <a class="dropdown-item" href="#">Another action</a>
                    <a class="dropdown-item" href="#">Something else here</a>
                    <div class="dropdown-divider"></div>
                    <a class="dropdown-item" href="#">Separated link</a>
                    </div>
                </li>
                </ul>
            </div>
            </div>
        </nav>
    );
};

