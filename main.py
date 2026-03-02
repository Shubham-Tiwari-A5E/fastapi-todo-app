from fastapi import FastAPI, Request
from database import check_database_connection
from routes.todoRoutes import router as todo_router
from users import router as user_router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    try:
        check_database_connection()
    except Exception as e:
        print(f"Database connection failed: {e}")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)
app.include_router(todo_router)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard")
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
