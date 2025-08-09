// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'static', // Output to Flask static folder
  },
  server: {
    proxy: {
      '/api': 'http://localhost:5000', // Proxy API calls to Flask
    },
  },
});