/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/**/*.html',
    '/src/js/main.js',
  ],
  theme: {
    extend: {
      spacing: {
        125: '31.25rem',
      },
      fontFamily: {
        sans: ['Avenir', 'ui-sans-serif', 'system-ui',],
        avenir: ['Avenir',],
        helvetica: ['Helvetica Neue',],
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

