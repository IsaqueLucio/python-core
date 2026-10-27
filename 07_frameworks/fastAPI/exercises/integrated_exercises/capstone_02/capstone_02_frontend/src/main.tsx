import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'

async function enableMocking() {
  if (!import.meta.env.DEV || import.meta.env.VITE_ENABLE_MOCKS !== 'true') {
    return false;
  }
  const { worker } = await import('./mocks/browser');
  await worker.start({
    onUnhandledRequest: 'bypass',
  });
  return true;
}

enableMocking()
  .then(() => {
    createRoot(document.getElementById('root')!).render(
      <StrictMode>
        <App />
      </StrictMode>,
    );
  })
  .catch((err) => {
    console.error("Mock Service Worker failed to start", err);
    document.getElementById('root')!.innerHTML = `
      <div style="font-family: system-ui, sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; padding: 2rem; text-align: center; background-color: #fef2f2; color: #991b1b;">
        <h1 style="font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem;">Failed to start application</h1>
        <p style="margin-bottom: 1.5rem;">The Mock Service Worker (MSW) failed to initialize. Please check your browser console for details.</p>
        <button onclick="window.location.reload()" style="padding: 0.5rem 1rem; background-color: #dc2626; color: white; border: none; border-radius: 0.25rem; cursor: pointer;">Retry Loading</button>
      </div>
    `;
  });
