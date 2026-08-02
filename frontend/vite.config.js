import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/site1': { target: 'http://localhost:8001', changeOrigin: true, rewrite: (path) => path.replace(/^\/api\/site1/, '') },
      '/api/site2': { target: 'http://localhost:8002', changeOrigin: true, rewrite: (path) => path.replace(/^\/api\/site2/, '') },
      '/api/site3': { target: 'http://localhost:8003', changeOrigin: true, rewrite: (path) => path.replace(/^\/api\/site3/, '') },
      '/api/site4': { target: 'http://localhost:8004', changeOrigin: true, rewrite: (path) => path.replace(/^\/api\/site4/, '') },
      '/api/tracker': { target: 'http://localhost:8007', changeOrigin: true, rewrite: (path) => path.replace(/^\/api\/tracker/, '') }
    }
  }
});
