# Todo App - Full Stack Application

## Overview
A beautiful, modern full-stack Todo application built with FastAPI, Jinja2 templates, MySQL, and comprehensive testing.

## Features
- ✅ User Authentication (JWT-based)
- ✅ User Registration & Login
- ✅ Create, Read, Update, Delete (CRUD) Todos
- ✅ Priority System (1-5)
- ✅ Mark tasks as complete/incomplete
- ✅ User-specific task isolation
- ✅ Beautiful responsive UI
- ✅ Comprehensive test suite
- ✅ **NEW:** Newest todos displayed at top
- ✅ **NEW:** Filter todos (All/Active/Completed)
- ✅ **NEW:** Hide edit/delete buttons on completed todos
- ✅ **NEW:** Green tick badge for completed todos
- ✅ **NEW:** Completion timestamp tracking and display

## Tech Stack
- **Backend**: FastAPI
- **Frontend**: HTML, CSS, JavaScript, Jinja2
- **Database**: MySQL
- **Authentication**: JWT (JSON Web Tokens)
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Testing**: pytest

## Installation

1. Create and activate virtual environment:
```bash
python -m venv fastapienv
fastapienv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install fastapi uvicorn sqlalchemy pymysql python-jose passlib pytest httpx requests jinja2
```

3. Setup MySQL database:
- Ensure MySQL is running
- Database credentials: user: root, password: raj1234
- Database will be created automatically on startup

## Running the Application

1. Start the server:
```bash
cd Todos
uvicorn main:app --reload
```

2. Access the application:
- Home: http://127.0.0.1:8000/
- API Docs: http://127.0.0.1:8000/docs
- Login: http://127.0.0.1:8000/login
- Register: http://127.0.0.1:8000/register
- Dashboard: http://127.0.0.1:8000/dashboard

## Running Tests

Run all tests:
```bash
pytest test/test_api.py -v
```

Run specific test:
```bash
pytest test/test_api.py::test_create_20_todos_and_validate -v
```

## Database Migrations

Create new migration:
```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations:
```bash
alembic upgrade head
```

## Project Structure
```
Todos/
├── main.py                 # FastAPI application entry point
├── database.py             # Database configuration
├── test_database.py        # Test database setup
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
├── auth.py                 # Authentication logic
├── users.py                # User routes
├── routes/
│   └── todoRoutes.py       # Todo API routes
├── controllers/
│   ├── todoController.py   # Todo business logic
│   └── user/
│       └── userController.py
├── services/
│   ├── todoService.py      # Todo database operations
│   └── user/
│       └── userService.py
├── templates/              # Jinja2 HTML templates
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── static/
│   ├── css/
│   │   └── style.css       # Application styles
│   └── js/
│       ├── login.js
│       ├── register.js
│       └── dashboard.js
├── test/
│   ├── test_example.py
│   └── test_api.py         # Comprehensive API tests
└── alembic/                # Database migrations
```

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /token` - Login and get JWT token

### Todos
- `GET /todos` - Get all todos for logged-in user
- `POST /todos` - Create new todo
- `GET /todos/{todo_id}` - Get specific todo
- `PUT /todos/{todo_id}` - Update todo
- `DELETE /todos/{todo_id}` - Delete todo

## Test Coverage

### User Tests
- User registration
- Duplicate email prevention
- Login with correct credentials
- Login with wrong password
- Login with non-existent user

### Todo Tests
- Create todo
- Create todo without authentication
- Create multiple todos
- Get all todos
- Get single todo
- Get non-existent todo
- Update todo
- Update non-existent todo
- Delete todo
- Delete non-existent todo

### Security Tests
- User isolation (users can only access their own todos)
- JWT authentication enforcement

### Functional Tests
- Priority system validation
- Toggle completion status
- Batch operations (create 20 todos and validate)

## Test Results
All 20 tests passed successfully! ✅

## Features Highlights

### Beautiful UI
- Modern gradient design
- Responsive layout
- Smooth animations
- Intuitive user interface

### Security
- Password hashing (PBKDF2-SHA256)
- JWT-based authentication
- User-specific data isolation
- Protected API endpoints

### Database
- MySQL with proper relationships
- User-Todo one-to-many relationship
- Alembic migrations for schema management
- Separate test database

## Usage

1. **Register**: Create a new account
2. **Login**: Authenticate with your credentials
3. **Dashboard**: View, create, edit, and delete your todos
4. **Manage Tasks**: 
   - Add new tasks with priorities (newest appear at top)
   - Mark tasks as complete
   - Edit task details
   - Delete completed tasks
   - **Filter tasks**: Use the filter buttons to view:
     - **All**: See all your tasks
     - **Active**: See only incomplete tasks
     - **Completed**: See only completed tasks

## Contributing
This is a learning project demonstrating FastAPI best practices.

## License
MIT License
