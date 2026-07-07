/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          50: '#eef5fb',
          100: '#d8e8f5',
          700: '#173b57',
          800: '#102a43',
          900: '#0b1f33',
        },
      },
      boxShadow: {
        soft: '0 18px 45px rgba(15, 23, 42, 0.08)',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'Segoe UI', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
