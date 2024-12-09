import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { NextUIProvider } from '@nextui-org/react';
import {useTheme} from "@nextui-org/use-theme";

// to let the theme follow the user settings  
function RootComponent() {
  // use hock - must inside function 
  const { theme } = useTheme();

  return (
      <main className={`${theme} light text-foreground bg-background w-screen h-screen p-4`}>
        <App />
      </main>
  );
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* wrap with app with using nextui */}
    <NextUIProvider>
        <RootComponent />
    </NextUIProvider>
  </StrictMode>,
)
