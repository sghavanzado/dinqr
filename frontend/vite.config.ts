import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  server: {
    host: '0.0.0.0', // Escuchar en todas las IPs del host
    port: 5173, // Puerto predeterminado
  },
  plugins: [react()],
})
