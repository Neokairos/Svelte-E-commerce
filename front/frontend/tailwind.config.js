module.exports = {
  content: [
    "./src/**/*.{svelte,js,ts}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        neopurple: {
        deLight: '#5B3F8D', // Dark shade of purple
        deBlack: '#3B3F5B', // Darker shade of purple
        }
      },
    },
    extend: {},
  },
  plugins: [],
}
