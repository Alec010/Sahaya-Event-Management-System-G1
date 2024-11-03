/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './users/templates/**/*.html', // Adjust to the path where your HTML files are located
    './users/static/**/*.css', // Include the CSS files
    './event/static/**/*.css' // Include the CSS files
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light"], // You can change the theme as needed
  },
}
