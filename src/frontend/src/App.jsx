import * as React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css'
import routes from './routes';
import {NextUIProvider} from "@nextui-org/react";
import {Navbar, NavbarBrand, NavbarContent, NavbarItem, Link, Button} from "@nextui-org/react";

const NotFoundPage = () => <h1 className="center">404 NOT FOUND!!</h1>

export const AcmeLogo = () => {
  return (
    <svg fill="none" height="36" viewBox="0 0 32 32" width="36">
      <path
        clipRule="evenodd"
        d="M17.6482 10.1305L15.8785 7.02583L7.02979 22.5499H10.5278L17.6482 10.1305ZM19.8798 14.0457L18.11 17.1983L19.394 19.4511H16.8453L15.1056 22.5499H24.7272L19.8798 14.0457Z"
        fill="currentColor"
        fillRule="evenodd"
      />
    </svg>
  );
};


export default function App() {
  return (
    <NextUIProvider>
      <Router>
        <Navbar>
          <NavbarBrand>
            <AcmeLogo />
            <p className="font-bold text-inherit">Bus Stop Crowd Detection</p>
          </NavbarBrand>
          <NavbarContent className="hidden sm:flex gap-4" justify="center">
            <NavbarItem>
              <Link color="foreground" href="#">
                HOME
              </Link>
            </NavbarItem>
            <NavbarItem isActive>
              <Link aria-current="page" href="#">
                Test
              </Link>
            </NavbarItem>
            <NavbarItem>
              <Link color="foreground" href="#">
                Integrations
              </Link>
            </NavbarItem>
          </NavbarContent>
          <NavbarContent justify="end">
            <NavbarItem className="hidden lg:flex">
              <Link href="#">Login</Link>
            </NavbarItem>
            <NavbarItem>
              <Button as={Link} color="primary" href="#" variant="flat">
                Sign Up
              </Button>
            </NavbarItem>
          </NavbarContent>
        </Navbar>
        <Routes>
          <Route path={routes.home} element={<NotFoundPage />} />
          <Route path={routes.bus} element={<NotFoundPage />} />
          <Route path="/bus/display" element={<NotFoundPage />} />
          <Route path="/test" element={<NotFoundPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Router>
    </NextUIProvider>
  );
}