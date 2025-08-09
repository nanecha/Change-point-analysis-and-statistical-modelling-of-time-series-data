// src/vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  root: '.', // Treat src/ as project root
  publicDir: 'public', // Use src/public/ for index.html
  build: {
    outDir: '../static', // Output to Flask static folder
    emptyOutDir: true, // Clear static/ before build
  },
  server: {
    proxy: {
      '/api': 'http://localhost:5000', // Proxy API calls to Flask
    },
  },
});