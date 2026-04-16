/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        lab: {
          bg:      '#0a0e0a',
          surface: '#0f150f',
          card:    '#141c14',
          border:  '#1e2e1e',
          green:   '#00ff41',
          dim:     '#00cc33',
          blue:    '#00b4ff',
          amber:   '#ffb300',
          red:     '#ff4444',
          purple:  '#cc88ff',
          text:    '#c8d8c8',
          muted:   '#4a6a4a',
        },
      },
      fontFamily: { mono: ['"JetBrains Mono"', 'Consolas', 'monospace'] },
    },
  },
  plugins: [],
}
