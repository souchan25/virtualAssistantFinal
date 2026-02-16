/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cpsu-green': '#006B3F',      // Earls Green - Primary
        'cpsu-yellow': '#FFF44F',      // Lemon Yellow - Secondary
        'cpsu-green-dark': '#004d2d',  // Darker shade for hover states
        'cpsu-yellow-dark': '#e6db3d', // Darker yellow for hover
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        heading: ['Poppins', 'Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
