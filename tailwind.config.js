/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/**/*.html'
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

