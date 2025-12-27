/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        streamlit: {
          bg: '#f0f2f6',     // Le gris clair de fond Streamlit
          sidebar: '#ffffff', // Le blanc de la sidebar
          primary: '#ff4b4b'  // Le rouge caractéristique de Streamlit
        }
      }
    },
  },
  plugins: [],
}