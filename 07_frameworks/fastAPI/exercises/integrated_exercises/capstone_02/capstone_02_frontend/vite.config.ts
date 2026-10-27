/// <reference types="vitest" />
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vitest/config'
import fs from 'fs'
import path from 'path'

function excludeMocksPlugin() {
  return {
    name: 'exclude-mocks',
    closeBundle() {
      const p = path.resolve(__dirname, 'dist/mockServiceWorker.js')
      if (fs.existsSync(p)) {
        fs.unlinkSync(p)
      }
    }
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss(), excludeMocksPlugin()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/setupTests.ts'],
    globals: true,
  }
})
