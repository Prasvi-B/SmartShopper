/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],

  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb', // Royal Blue
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        emerald: {
          50: '#ecfdf5',
          100: '#d1fae5',
          200: '#a7f3d0',
          300: '#6ee7b7',
          400: '#34d399',
          500: '#10b981', // Emerald Green
          600: '#059669',
          700: '#047857',
          800: '#065f46',
          900: '#064e3b',
        },
        amber: {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b', // Amber/Yellow
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f',
        },
        slate: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155', // Slate Gray
          800: '#1e293b',
          900: '#0f172a',
        },
        accent: {
          blue: '#2563EB',
          purple: '#7C3AED',
          cyan: '#06b6d4',
          pink: '#ec4899',
        },
        dark: {
          bg: '#0f0f23',
          card: '#1a1a2e',
          surface: '#16213e',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        glow: '0 0 20px rgba(37,99,235,0.4), 0 0 40px rgba(37,99,235,0.1)',
        'glow-lg': '0 0 30px rgba(37,99,235,0.5), 0 0 60px rgba(37,99,235,0.2)',
        glass: '0 8px 32px 0 rgba(31, 41, 55, 0.37)',
        'glass-lg': '0 12px 40px 0 rgba(31, 41, 55, 0.5)',
        neon: '0 0 5px theme(colors.accent.blue), 0 0 20px theme(colors.accent.blue), 0 0 30px theme(colors.accent.blue)',
      },
      backgroundImage: {
        'gradient-accent': 'linear-gradient(135deg, #2563EB 0%, #7C3AED 100%)',
        'gradient-glass': 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
        'gradient-glow': 'radial-gradient(circle, rgba(37,99,235,0.1) 0%, transparent 70%)',
      },
      backdropBlur: {
        xs: '2px',
        sm: '4px',
        md: '8px',
        lg: '12px',
        xl: '16px',
      },
      backdropSaturate: {
        180: '1.8',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInLeft: {
          '0%': { opacity: '0', transform: 'translateX(-30px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        glow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(37,99,235,0.4)' },
          '50%': { boxShadow: '0 0 30px rgba(37,99,235,0.6), 0 0 40px rgba(124,58,237,0.3)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        pop: {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.05)' },
          '100%': { transform: 'scale(1)' },
        },
      },
      animation: {
        fadeInUp: 'fadeInUp 0.8s cubic-bezier(0.4,0,0.2,1)',
        slideInLeft: 'slideInLeft 0.6s cubic-bezier(0.4,0,0.2,1)',
        shimmer: 'shimmer 2s infinite linear',
        glow: 'glow 2s ease-in-out infinite alternate',
        float: 'float 3s ease-in-out infinite',
        pop: 'pop 0.3s cubic-bezier(0.4,0,0.2,1)',
      },
    },
  },
  darkMode: 'class',
  plugins: [],
}