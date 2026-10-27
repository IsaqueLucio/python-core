# HelpDesk REST API Contract

This document outlines the exact REST API contract that the frontend expects the backend to implement.

## Base URL
All endpoints are relative to `VITE_API_BASE_URL` (default: `http://localhost:8000`).

## Authentication & Authorization
- The API uses OAuth2 with Bearer Tokens (JWT).
- Protected endpoints require an `Authorization: Bearer <token>` header.
- Roles: `customer`, `agent`, `admin`.
- Inactive users (`is_active: false`) must receive `401 Unauthorized`.

---

## Auth Endpoints

### 1. Login
- **Method:** `POST`
- **Path:** `/auth/login`
- **Content-Type:** `application/x-www-form-urlencoded`
- **Request Body:**
  - `username` (string)
  - `password` (string)
- **Response (200 OK):**
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```
- **Errors:** 401 (Invalid credentials or inactive user).

### 2. Register
- **Method:** `POST`
- **Path:** `/auth/register`
- **Content-Type:** `application/json`
- **Request Body:**
  ```json
  {
    "name": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Response (201 Created):** User object.
- **Errors:** 409 (Email already registered).

### 3. Get Current User
- **Method:** `GET`
- **Path:** `/auth/me`
- **Response (200 OK):** User object.

---

## Tickets Endpoints

### 4. List Tickets
- **Method:** `GET`
- **Path:** `/tickets`
- **Query Parameters:**
  - `page` (int, default: 1)
  - `page_size` (int, default: 10)
  - `search` (string, optional)
  - `status` (string, optional)
  - `priority` (string, optional)
  - `category` (string, optional)
  - `assigned_to_me` (boolean, optional)
- **Permissions:** 
  - Admin: all
  - Agent: unassigned or assigned to them
  - Customer: created by them
- **Sorting:** `created_at DESC`, `id DESC`.
- **Response (200 OK):**
  ```json
  {
    "items": [ /* Ticket objects */ ],
    "page": 1,
    "page_size": 10,
    "total": 100,
    "total_pages": 10
  }
  ```

### 5. Get Ticket
- **Method:** `GET`
- **Path:** `/tickets/:id`
- **Response (200 OK):** Ticket object.
- **Errors:** 403 (Forbidden), 404 (Not Found).

### 6. Create Ticket
- **Method:** `POST`
- **Path:** `/tickets`
- **Request Body:**
  ```json
  {
    "title": "string",
    "description": "string",
    "priority": "low|medium|high|urgent",
    "category": "hardware|software|network|access|other"
  }
  ```
- **Response (201 Created):** Ticket object.

### 7. Update Ticket
- **Method:** `PATCH`
- **Path:** `/tickets/:id`
- **Request Body:** Partial Ticket fields (e.g. `status`, `priority`).
- **Permissions:** Admin (any), Agent (if assigned to them), Customer (if creator AND status is 'open'). Customers cannot change `status` unprivileged.
- **Response (200 OK):** Updated Ticket object.

### 8. Assign Ticket
- **Method:** `PATCH`
- **Path:** `/tickets/:id/assign`
- **Request Body:**
  ```json
  {
    "agent_id": 123
  }
  ```
- **Permissions:** Admin (assign to any active agent or self), Agent (assign to self only if unassigned).
- **Response (200 OK):** Updated Ticket object.

### 9. Delete Ticket
- **Method:** `DELETE`
- **Path:** `/tickets/:id`
- **Permissions:** Admin (any), Customer (creator, only if 'open').
- **Response:** `204 No Content`.

---

## Comments Endpoints

### 10. List Comments
- **Method:** `GET`
- **Path:** `/tickets/:id/comments`
- **Permissions:** Same as viewing ticket.
- **Response (200 OK):** Array of TicketComment objects.

### 11. Add Comment
- **Method:** `POST`
- **Path:** `/tickets/:id/comments`
- **Request Body:**
  ```json
  {
    "content": "string"
  }
  ```
- **Permissions:** Same as viewing ticket.
- **Response (201 Created):** TicketComment object.

---

## Dashboard Endpoints

### 12. Dashboard Summary
- **Method:** `GET`
- **Path:** `/dashboard/summary`
- **Response (200 OK):**
  ```json
  {
    "total_tickets": 0,
    "open_tickets": 0,
    "in_progress_tickets": 0,
    "waiting_customer_tickets": 0,
    "resolved_tickets": 0,
    "closed_tickets": 0,
    "urgent_tickets": 0,
    "my_assigned_tickets": 0
  }
  ```

---

## Users Endpoints (Admin Only)

### 13. List Users
- **Method:** `GET`
- **Path:** `/users`
- **Query Parameters:** `page`, `page_size`, `search`, `role`, `is_active`
- **Response (200 OK):** Paginated User items.

### 14. Update User
- **Method:** `PATCH`
- **Path:** `/users/:id`
- **Request Body:** Partial User (e.g., `role`, `is_active`).
- **Response (200 OK):** Updated User.

---

## Domain Models

### User
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "customer|agent|admin",
  "is_active": true,
  "created_at": "2023-10-01T12:00:00Z"
}
```

### Ticket
```json
{
  "id": 1,
  "title": "Cannot login",
  "description": "Password reset is not working...",
  "status": "open|in_progress|waiting_customer|resolved|closed",
  "priority": "low|medium|high|urgent",
  "category": "hardware|software|network|access|other",
  "created_by": { "id": 1, "name": "John", "email": "john@example.com", "role": "customer" },
  "assigned_to": null, // or User Summary Object
  "created_at": "2023-10-01T12:00:00Z",
  "updated_at": "2023-10-01T12:00:00Z"
}
```

### TicketComment
```json
{
  "id": 1,
  "content": "I'm looking into this.",
  "author": { "id": 2, "name": "Agent Smith", "email": "smith@example.com", "role": "agent" },
  "created_at": "2023-10-01T12:30:00Z"
}
```
