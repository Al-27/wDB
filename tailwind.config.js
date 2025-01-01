/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./flask_app/**/*.{html,js}"],
  theme: {
    extend: {
      gridTemplateColumns:{
        'wdb2' : 'minmax(4rem, 12rem) minmax(75%,100%)'   
      },
      gridTemplateRows:{
        'wdb2' : 'minmax(4rem, 6rem) 75%;'  
      },
      boxShadow:{
        //innerSmall
        'is': '0 0 1px 1px rgba(0,0,0,.3)' 
      },
      height:{
        '21': '5.25rem',
        '22': '5.5rem',
        '23': '5.75rem'
      },
      lineHeight:{
        '2': '.5rem'
      }
    },
  },
  plugins: [],
}

