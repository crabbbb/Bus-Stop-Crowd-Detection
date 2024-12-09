/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "rgb(43 106 70)", 
        secondary: "#b5ccb9",  
        success: "#94d5a9",   
        warning: "#f5a524",   
        danger: "#f31260",    
        background: "#F8F9FA",  
        foreground: "#212529", 
      },
      fontFamily: {
        sans: ["Roboto", "sans-serif"],
      },
    },
  },
  plugins: [],
}

