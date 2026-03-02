# FastAPI Todo Application

A production-ready, full-stack Todo application built with FastAPI, MySQL, JWT authentication, and a beautiful responsive UI.

## 🌟 Features

- ✅ **User Authentication** - JWT-based secure authentication
- ✅ **User Registration & Login** - Complete user management system
- ✅ **CRUD Operations** - Create, Read, Update, Delete todos
- ✅ **Priority System** - 5-level priority for task organization
- ✅ **Task Completion** - Mark tasks as complete/incomplete with timestamp tracking
- ✅ **User Isolation** - Each user can only access their own todos
- ✅ **Beautiful UI** - Modern, responsive design with Jinja2 templates
- ✅ **Filtering** - Filter by All/Active/Completed todos
- ✅ **Newest First** - Automatic chronological sorting
- ✅ **Visual Indicators** - Green tick badge for completed todos
- ✅ **Completion Tracking** - Timestamp and display of completion date
- ✅ **Protected Actions** - Edit/Delete buttons hidden for completed todos
- ✅ **Comprehensive Testing** - 28+ tests with pytest

## 🚀 Tech Stack

- **Backend**: FastAPI (Python 3.14)
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens) with python-jose
- **Password Hashing**: Passlib with bcrypt
- **Frontend**: HTML, CSS, JavaScript (Vanilla JS)
- **Templates**: Jinja2
- **Migrations**: Alembic
- **Testing**: pytest with test database

## 📋 Prerequisites

- Python 3.14+
- MySQL Server
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/fastapi-todo-app.git
cd fastapi-todo-app
```

### 2. Create and activate virtual environment

```bash
# Windows
python -m venv fastapienv
fastapienv\Scripts\activate

# Linux/Mac
python3 -m venv fastapienv
source fastapienv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy pymysql python-jose passlib bcrypt pytest httpx requests jinja2 alembic
```

### 4. Configure database

Update database credentials in `database.py`:
```python
DATABASE_URL = "mysql+pymysql://root:your_password@localhost/todos"
```

### 5. Run migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn main:app --reload
```

The application will be available at: `http://127.0.0.1:8000`

## 📁 Project Structure

```
Todos/
├── main.py                     # Application entry point
├── database.py                 # Database configuration
├── test_database.py            # Test database setup
├── models.py                   # SQLAlchemy models
├── schemas.py                  # Pydantic schemas
├── auth.py                     # Authentication logic
├── users.py                    # User routes
├── routes/
│   └── todoRoutes.py           # Todo API routes
├── controllers/
│   ├── todoController.py       # Todo business logic
│   └── user/
│       └── userController.py   # User controller
├── services/
│   ├── todoService.py          # Todo database operations
│   └── user/
│       └── userService.py      # User service
├── templates/                  # Jinja2 HTML templates
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── static/
│   ├── css/
│   │   └── style.css           # Application styles
│   └── js/
│       ├── login.js
│       ├── register.js
│       └── dashboard.js
├── test/
│   ├── test_api.py             # API tests (20 tests)
│   ├── test_completed_at.py    # Completion tracking tests (6 tests)
│   └── test_new_features.py    # Feature tests (2 tests)
└── alembic/                    # Database migrations
    └── versions/
```

## 🔑 API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /token` - Login and get JWT token

### Todos
- `GET /todos` - Get all todos for authenticated user
- `POST /todos` - Create new todo
- `GET /todos/{todo_id}` - Get specific todo
- `PUT /todos/{todo_id}` - Update todo
- `DELETE /todos/{todo_id}` - Delete todo

### Frontend Pages
- `GET /` - Home page
- `GET /login` - Login page
- `GET /register` - Registration page
- `GET /dashboard` - Todo dashboard (requires authentication)

## 🧪 Testing

Run all tests:
```bash
pytest test/ -v
```

Run specific test file:
```bash
pytest test/test_api.py -v
pytest test/test_completed_at.py -v
```

### Test Coverage
- ✅ User registration and authentication
- ✅ Todo CRUD operations
- ✅ User data isolation
- ✅ Completion timestamp tracking
- ✅ Filter functionality
- ✅ Priority validation
- ✅ **Total: 28 tests passing**

## 🎨 Features Showcase

### Completed Todo Enhancement
- **Green Tick Badge**: Visual indicator (✓ Completed) on completed todos
- **Completion Timestamp**: Tracks and displays when todo was completed
- **Protected Actions**: Edit/Delete buttons hidden for completed todos
- **Beautiful Design**: Green theme with professional styling

### Todo Filtering
- **All**: View all your todos
- **Active**: View only incomplete todos
- **Completed**: View only completed todos

### Smart Sorting
- Newest todos automatically appear at the top
- Chronological ordering by creation date

## 🔐 Security

- Password hashing with bcrypt
- JWT token-based authentication
- User-specific data isolation
- Protected API endpoints
- XSS prevention in frontend

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);
```

### Todos Table
```sql
CREATE TABLE todos (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    priority INT NOT NULL,
    isCompleted BOOLEAN DEFAULT FALSE,
    user_id VARCHAR(36) NOT NULL,
    created_at DATETIME NOT NULL,
    completed_at DATETIME NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 🚀 Deployment

### Production Checklist
- [ ] Update database credentials
- [ ] Set strong JWT secret key
- [ ] Configure CORS settings
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure database backups
- [ ] Set up monitoring

## 📝 Usage

1. **Register** a new account
2. **Login** with your credentials
3. **Dashboard** - View and manage your todos
4. **Create** todos with title, description, and priority
5. **Filter** by All/Active/Completed
6. **Complete** todos to see the green checkmark
7. **Edit/Delete** active todos as needed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Built as a learning project to demonstrate FastAPI best practices.

## 🙏 Acknowledgments

- FastAPI documentation
- SQLAlchemy documentation
- Python community

## 📚 Documentation

Additional documentation available in:
- `COMPLETED_TODOS_ENHANCEMENT.md` - Detailed feature documentation
- `DEMO.md` - Visual demonstration guide
- `IMPLEMENTATION_SUMMARY.md` - Complete implementation summary
- `NEW_FEATURES.md` - New features documentation

## 🐛 Known Issues

None currently. All 28 tests passing! ✅

## 🔮 Future Enhancements

- [ ] Email notifications
- [ ] Task categories/tags
- [ ] Subtasks support
- [ ] File attachments
- [ ] Collaboration features
- [ ] Mobile app
- [ ] Dark mode

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**⭐ If you find this project helpful, please consider giving it a star!**
