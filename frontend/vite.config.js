import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Workaround plugin: rewrite '/' to '/index.html' so browsers get the
// application page instead of a 404 in some dev environments.
function ensureRootIndexPlugin() {
  return {
    name: 'ensure-root-index',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        if (req.url === '/' || req.url === '') {
          req.url = '/index.html'
        }
        next()
      })
    }
  }
}

// https://vitejs.dev/config/
export default defineConfig({
  // Disable fast refresh to avoid runtime preamble detection issues seen in
  // some dev environments (the UI will still hot-reload on full reloads).
  plugins: [react({ fastRefresh: false }), ensureRootIndexPlugin()],
  server: {
    port: 3000,
    proxy: {
      // Proxy API calls to the backend FastAPI server
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})