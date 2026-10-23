# School Student Information System

A modern school management platform starter built for managing students, attendance, assessments, fees, and dashboards.

## Tech stack
- Frontend: React + Vite
- Backend: Node.js + Express
- Database: PostgreSQL-ready schema (starter API included)
- Auth: RBAC-ready structure
- Dashboard: mock analytics for admin and student views

## Features included
- Student directory
- Attendance overview
- Gradebook data
- Fee summary
- Admin dashboard analytics
- Parent/student dashboard summary
- Basic REST API ready for expansion

## Project structure
- `backend/` — Express API and mock data
- `frontend/` — React dashboard UI
- `README.md` — setup and usage guide

## Quick start

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the application in development mode:
   ```bash
   npm run dev
   ```

3. Open the frontend in your browser:
   - `http://localhost:5173`

4. API is available at:
   - `http://localhost:5000/api/health`
   - `http://localhost:5000/api/dashboard`
   - `http://localhost:5000/api/students`

## Production-ready roadmap
- Add real PostgreSQL schema and migrations
- Implement JWT authentication and RBAC
- Integrate payment gateway, SMS, and email alerts
- Add teacher/admin authorization flows
- Create school-wide reporting and analytics

## License
MIT
