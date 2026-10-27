# HelpDesk Frontend

HelpDesk is a modern, responsive React frontend application designed for technical support ticket management. It is built as a capstone exercise for integrating a React frontend with a FastAPI backend.

This project is currently completely decoupled from any specific backend, and runs independently using Mock Service Worker (MSW) to simulate API interactions.

## Technology Stack

- **Framework:** React + TypeScript (Vite)
- **Routing:** React Router
- **Data Fetching:** Axios + TanStack Query (React Query)
- **Forms & Validation:** React Hook Form + Zod
- **Styling:** Tailwind CSS + Lucide React icons
- **Testing:** Vitest + React Testing Library
- **API Mocking:** Mock Service Worker (MSW)

## Folder Structure

```
capstone_02_frontend/
├── src/
│   ├── api/           # Axios instance and API service functions
│   ├── components/    # Reusable UI, Layout, and Feedback components
│   ├── contexts/      # Auth and Theme providers
│   ├── mocks/         # MSW server, handlers, and in-memory database
│   ├── pages/         # Application views (Dashboard, Tickets, etc.)
│   ├── routes/        # Route guards (ProtectedRoute, RoleRoute)
│   ├── types/         # Domain TypeScript interfaces
│   ├── __tests__/     # Vitest test suites
│   ├── App.tsx        # Main application component & routing setup
│   └── main.tsx       # Entry point
```

## Setup and Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Environment Configuration:**
   Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

   Make sure your `.env` contains:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   VITE_ENABLE_MOCKS=true
   ```
   *Note: Set `VITE_ENABLE_MOCKS=true` to run the application with the in-memory mock backend.*

3. **Run the Development Server:**
   ```bash
   npm run dev
   ```

## Roles and Permissions

The system supports three user roles:
- **Customer:** Can create and view their own tickets, and add comments.
- **Support Agent:** Can view all tickets, assign tickets to themselves, change status/priority, and add comments.
- **Administrator:** Has all agent permissions, plus the ability to manage users (activate/deactivate and change roles).

## Demo Credentials (Mock Mode)

When running with `VITE_ENABLE_MOCKS=true`, you can use the following mock accounts:

- **Customer:**
  - Email: `customer@example.com`
  - Password: `customer123`
- **Support Agent:**
  - Email: `agent@example.com`
  - Password: `agent123`
- **Administrator:**
  - Email: `admin@example.com`
  - Password: `admin123`

## Connecting to FastAPI

When your FastAPI backend is ready, follow these steps to connect the frontend to the real backend:

1. Update `.env` to disable mocks:
   ```env
   VITE_ENABLE_MOCKS=false
   VITE_API_BASE_URL=http://localhost:8000  # Adjust to your FastAPI URL
   ```
2. Ensure your FastAPI application is running.
3. Configure CORS on your FastAPI server to accept requests from the frontend development server (`http://localhost:5173`).

## Testing and Building

**Run the test suite:**
```bash
npm run test
```

**Run the production build:**
```bash
npm run build
```
*Note: The `mockServiceWorker.js` file is automatically excluded from the production `dist/` folder via Vite configuration. The mock backend will never ship to production.*

**Preview the production build:**
```bash
npm run preview
```

## Troubleshooting

- **CORS Errors:** If you see CORS errors in the console when connecting to your FastAPI backend, ensure you have correctly added `http://localhost:5173` to the `CORSMiddleware` `allow_origins` array in your FastAPI application.
- **401 Unauthorized:** If your session expires or your token is invalid, the frontend's Axios interceptor will automatically log you out and redirect you to the login page.
- **API Unavailability:** If the backend is down, standard network errors will be caught and displayed gracefully via toast notifications or error states within the UI components.
