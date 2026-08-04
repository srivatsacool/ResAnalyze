/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin');
module.exports = {
  content: ['./src/**/*.{astro,jsx,tsx,ts,md,mdx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        base: '#05050A',
        void: '#05050A',
        primary: '#ECECF4',
        neon: '#22D3EE',
        violetx: '#8B5CF6',
        cyanx: '#22D3EE',
        goldx: '#E9B949',
        ink: '#ECECF4',
        mute: '#8A8AA0',
      },
      fontFamily: {
        display: ['"JetBrains Mono"', 'monospace'],
        body: ['"Hanken Grotesk"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      keyframes: {
        pulse: { '0%,100%': { opacity: '1' }, '50%': { opacity: '0.35' } },
        float: { '0%,100%': { transform: 'translateY(0px)' }, '50%': { transform: 'translateY(-10px)' } },
        marquee: { to: { transform: 'translateX(-50%)' } },
        drift1: {
          '0%,100%': { transform: 'translate(0,0) scale(1)' },
          '33%': { transform: 'translate(70px,50px) scale(1.15)' },
          '66%': { transform: 'translate(-40px,90px) scale(0.95)' },
        },
        drift2: {
          '0%,100%': { transform: 'translate(0,0) scale(1)' },
          '40%': { transform: 'translate(-80px,-60px) scale(1.2)' },
          '75%': { transform: 'translate(40px,-20px) scale(0.9)' },
        },
        drift3: {
          '0%,100%': { transform: 'translate(0,0) scale(1)' },
          '50%': { transform: 'translate(-100px,-70px) scale(1.25)' },
        },
        shimmer: { to: { backgroundPosition: '200% center' } },
        laser: {
          '0%': { left: '-100%' },
          '100%': { left: '100%' },
        },
      },
      animation: {
        pulse: 'pulse 2s ease-in-out infinite',
        'float-slow': 'float 6s ease-in-out infinite',
        marquee: 'marquee 28s linear infinite',
        'drift-1': 'drift1 30s ease-in-out infinite',
        'drift-2': 'drift2 26s ease-in-out infinite',
        'drift-3': 'drift3 34s ease-in-out infinite',
        shimmer: 'shimmer 3.5s linear infinite',
      },
    },
  },
  plugins: [
    plugin(function({ addUtilities }) {
      addUtilities({
        '.glass': {
          'background': 'rgba(255,255,255,0.04)',
          '-webkit-backdrop-filter': 'blur(20px) saturate(180%)',
          'backdrop-filter': 'blur(20px) saturate(180%)',
          'border': '1px solid rgba(255,255,255,0.08)',
          'box-shadow': 'inset 0 1px 0 rgba(255,255,255,0.08), 0 8px 40px rgba(0,0,0,0.45)',
        },
        '.glass-deep': {
          'background': 'rgba(10,10,18,0.62)',
          '-webkit-backdrop-filter': 'blur(24px) saturate(160%)',
          'backdrop-filter': 'blur(24px) saturate(160%)',
          'border': '1px solid rgba(255,255,255,0.08)',
          'box-shadow': 'inset 0 1px 0 rgba(255,255,255,0.06), 0 24px 80px rgba(0,0,0,0.6)',
        },
        '.glass-card': {
          '@apply glass rounded-2xl p-8': {},
        },
        '.btn-primary': {
          'background': 'linear-gradient(135deg, #8B5CF6 0%, #22D3EE 100%)',
          'box-shadow': '0 0 32px rgba(139,92,246,0.35), 0 8px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.25)',
          'transition': 'transform .2s ease, box-shadow .2s ease, filter .2s ease',
        },
        '.btn-primary:hover': {
          'transform': 'translateY(-1px)',
          'filter': 'brightness(1.08)',
          'box-shadow': '0 0 44px rgba(139,92,246,0.5), 0 10px 28px rgba(0,0,0,0.45)',
        },
        '.btn-ghost': {
          'border': '1px solid rgba(255,255,255,0.14)',
          'background': 'rgba(255,255,255,0.03)',
          'transition': 'all .2s ease',
        },
        '.btn-ghost:hover': {
          'background': 'rgba(255,255,255,0.07)',
          'border-color': 'rgba(255,255,255,0.22)',
        },
        '.grad-text': {
          'background': 'linear-gradient(120deg, #A78BFA 0%, #22D3EE 100%)',
          '-webkit-background-clip': 'text',
          'background-clip': 'text',
          'color': 'transparent',
        },
        '.gold-text': { 'color': '#E9B949' },
        '.laser-sweep': {
          'position': 'relative',
          'overflow': 'hidden',
        },
        '.laser-sweep::after': {
          'content': '""',
          'position': 'absolute',
          'top': '0', 'left': '-100%',
          'width': '100%', 'height': '100%',
          'background': 'linear-gradient(90deg, transparent, rgba(34,211,238,0.25), transparent)',
          'animation': 'laser 2s infinite',
        },
      });
    }),
  ],
};
