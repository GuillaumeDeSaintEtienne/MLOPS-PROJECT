import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: [
      'xsiipwhc5v.eu-west-3.awsapprunner.com',
      'umvpvxmfsv.eu-west-3.awsapprunner.com'
    ],
    host: true,
    port: 8080
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './tests/setup.js', 
  }
})
