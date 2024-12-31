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
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

