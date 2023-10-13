/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin');
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  variants: {
    extend: {
      visibility: ['group-hover'],
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    plugin(function ({ addUtilities }) {  
      const newUtilities = {  
        '.hide-scrollbar::-webkit-scrollbar': {  
          display: 'none',  
        },
        '.hide-scrollbar:hover::-webkit-scrollbar': {  
          display: 'block',  
        },
        '.hide-scrollbar': {  
          '-ms-overflow-style': 'none',  
          'scrollbar-width': 'none',  
        },  
        '.hide-scrollbar:hover': {  
          '-ms-overflow-style': 'auto',  
          'scrollbar-width': 'auto',  
        },
      }  
      addUtilities(newUtilities, ['responsive'])  
    }),
  ],
  important: true
};
