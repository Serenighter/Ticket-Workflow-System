# Ticket Workflow System - Company Problem Reporting Solution
A comprehensive ticket management web application built with Django REST Framework backend and Vue.js frontend for efficient problem reporting within a company

## Features
- JWT authorization
- Roles (superuser, manager, staff)
- Create, delete tickets
- Different categories of issues
- Departments, employee departmetn associations
- Real-time ticket tracking

### Permissions
- Superusers: Full system access, department creation, user creation, all tickets
- Managers: Department-specific tickets, user assignment
- Employees: Department ticket visibility

### Empty dashboard
![Capture](https://github.com/user-attachments/assets/1467d86c-4271-4946-af03-00d5a66e1bbf)

### Dashboard with ticket details
![Capture12345](https://github.com/user-attachments/assets/cd7a478d-c7d7-4761-8b54-f82c2ce7f4c8)

### Form for creating a ticket
![Capture123](https://github.com/user-attachments/assets/c98164b9-eb2a-478b-8f8f-b9071c8eadeb)


## Technology Stack
### Backend
- Django 5.2
- Django REST Framework
- SQLite
- Python 3.11

### Frontend
- Vue.js 3.5
- Typescript
- Vite 6.2.5
- Pinia 3.0.2
- Vue Router 4.5.0
- Axios 1.8.4
- Chart.js 4.4.8

# Installation
### Prerequisites
- Python 3.11 or higher
- Node.js 22.14.0
- npm or yarn package manager
- Git

### Backend setup - Django
1. Clone repository <br>
  git clone https://github.com/Serenighter/Ticket-Workflow-System.git <br>
  cd ticketworkflow

2. Create python virtual environment (optional, recommended) <br>
   python -m venv env <br>
   source venv/bin/activate <br>
   _Windows:_ venv/Scripts/activate

3. Install Python dependencies <br>
  pip install django djangorestframework djangorestframework-simplejwt

4. Configure the database <br>
  python manage.py migrate

5. Create a superuser <br>
  python manage.py createsuperuser

6. Run development server <br>
  python manage.py runserver
  The Django API will be available at http://localhost:8000/api/

7. Setup departments and users <br>
  Create users and at least one department via the admin panel at http://127.0.0.1:8000/admin/

### Frontend Setup - Vue.js
1. Navigate to frontend directory <br>
   cd frontend <br>
   cd ticketworkflowfrontend

2. Install node.js dependencies <br>
   npm install

3. Run development server
   npm run dev
   The Vue.js application will be available at http://localhost:5173

## API Endpoints
### Authentication

POST /api/auth/register/ - User registration (only on backend)
POST /api/auth/login/ - User login
POST /api/auth/refresh/ - Token refresh

### Tickets

GET /api/tickets/ - List tickets
POST /api/tickets/ - Create ticket
GET /api/tickets/{id}/ - Get ticket details
POST /api/tickets/{id}/assign/ - Assign ticket
POST /api/tickets/{id}/close/ - Close ticket

### Users & Departments

GET /api/users/ - List users
GET /api/users/me/ - Current user profile
GET /api/departments/ - List departments
GET /api/dashboard/stats/ - Dashboard statistics
#
*Note: This is a development version. For production deployment, ensure proper security configurations, environment variables, and database setup.*
