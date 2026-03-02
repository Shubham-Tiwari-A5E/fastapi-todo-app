import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app
from database import get_db
from test_database import get_test_db, setup_test_database, teardown_test_database

# Override the get_db dependency
app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    """Setup and teardown for all tests"""
    setup_test_database()
    yield
    teardown_test_database()

@pytest.fixture
def test_user():
    """Create a test user"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPassword123"
    }
    response = client.post("/register", json=user_data)
    return user_data

@pytest.fixture
def auth_token(test_user):
    """Get authentication token"""
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    response = client.post("/token", data=login_data)
    return response.json()["access_token"]

@pytest.fixture
def auth_headers(auth_token):
    """Get authorization headers"""
    return {"Authorization": f"Bearer {auth_token}"}

# Test User Registration
def test_user_registration():
    """Test user registration endpoint"""
    user_data = {
        "name": "New User",
        "email": "newuser@example.com",
        "password": "SecurePass123"
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
    assert "id" in data

def test_duplicate_user_registration(test_user):
    """Test that duplicate email registration fails"""
    response = client.post("/register", json=test_user)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()

# Test User Login
def test_user_login(test_user):
    """Test user login endpoint"""
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_with_wrong_password(test_user):
    """Test login with incorrect password"""
    login_data = {
        "username": test_user["email"],
        "password": "WrongPassword"
    }
    response = client.post("/token", data=login_data)
    assert response.status_code == 401

def test_login_with_nonexistent_user():
    """Test login with non-existent user"""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "password"
    }
    response = client.post("/token", data=login_data)
    assert response.status_code == 401

# Test Todo Creation
def test_create_todo(auth_headers):
    """Test creating a new todo"""
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo",
        "priority": 3,
        "isCompleted": False
    }
    response = client.post("/todos", json=todo_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["priority"] == todo_data["priority"]
    assert "id" in data

def test_create_todo_without_auth():
    """Test creating todo without authentication fails"""
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo",
        "priority": 3,
        "isCompleted": False
    }
    response = client.post("/todos", json=todo_data)
    assert response.status_code == 401

def test_create_multiple_todos(auth_headers):
    """Test creating multiple todos"""
    for i in range(1, 6):
        todo_data = {
            "title": f"Todo {i}",
            "description": f"Description {i}",
            "priority": i,
            "isCompleted": False
        }
        response = client.post("/todos", json=todo_data, headers=auth_headers)
        assert response.status_code == 200

# Test Get Todos
def test_get_todos(auth_headers):
    """Test retrieving all todos for logged-in user"""
    # Create a todo first
    todo_data = {
        "title": "Get Test Todo",
        "description": "Test",
        "priority": 1,
        "isCompleted": False
    }
    client.post("/todos", json=todo_data, headers=auth_headers)

    response = client.get("/todos", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_todos_without_auth():
    """Test getting todos without authentication fails"""
    response = client.get("/todos")
    assert response.status_code == 401

# Test Get Single Todo
def test_get_single_todo(auth_headers):
    """Test retrieving a single todo by ID"""
    # Create a todo first
    todo_data = {
        "title": "Single Todo Test",
        "description": "Test",
        "priority": 2,
        "isCompleted": False
    }
    create_response = client.post("/todos", json=todo_data, headers=auth_headers)
    todo_id = create_response.json()["id"]

    response = client.get(f"/todos/{todo_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == todo_data["title"]

def test_get_nonexistent_todo(auth_headers):
    """Test getting a non-existent todo"""
    response = client.get("/todos/nonexistent-id", headers=auth_headers)
    assert response.status_code == 404

# Test Update Todo
def test_update_todo(auth_headers):
    """Test updating a todo"""
    # Create a todo first
    todo_data = {
        "title": "Original Title",
        "description": "Original Description",
        "priority": 1,
        "isCompleted": False
    }
    create_response = client.post("/todos", json=todo_data, headers=auth_headers)
    todo_id = create_response.json()["id"]

    # Update the todo
    updated_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "priority": 5,
        "isCompleted": True
    }
    response = client.put(f"/todos/{todo_id}", json=updated_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_data["title"]
    assert data["priority"] == updated_data["priority"]
    assert data["isCompleted"] == updated_data["isCompleted"]

def test_update_nonexistent_todo(auth_headers):
    """Test updating a non-existent todo"""
    updated_data = {
        "title": "Updated",
        "description": "Test",
        "priority": 1,
        "isCompleted": False
    }
    response = client.put("/todos/nonexistent-id", json=updated_data, headers=auth_headers)
    assert response.status_code == 404

# Test Delete Todo
def test_delete_todo(auth_headers):
    """Test deleting a todo"""
    # Create a todo first
    todo_data = {
        "title": "To Be Deleted",
        "description": "This will be deleted",
        "priority": 1,
        "isCompleted": False
    }
    create_response = client.post("/todos", json=todo_data, headers=auth_headers)
    todo_id = create_response.json()["id"]

    # Delete the todo
    response = client.delete(f"/todos/{todo_id}", headers=auth_headers)
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/todos/{todo_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_delete_nonexistent_todo(auth_headers):
    """Test deleting a non-existent todo"""
    response = client.delete("/todos/nonexistent-id", headers=auth_headers)
    assert response.status_code == 404

# Test User Isolation
def test_user_cannot_access_other_users_todos():
    """Test that users can only access their own todos"""
    # Create first user and todo
    user1_data = {
        "name": "User 1",
        "email": "user1@example.com",
        "password": "Password1"
    }
    client.post("/register", json=user1_data)
    login1_response = client.post("/token", data={
        "username": user1_data["email"],
        "password": user1_data["password"]
    })
    token1 = login1_response.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    todo_response = client.post("/todos", json={
        "title": "User 1 Todo",
        "description": "Test",
        "priority": 1,
        "isCompleted": False
    }, headers=headers1)
    todo_id = todo_response.json()["id"]

    # Create second user
    user2_data = {
        "name": "User 2",
        "email": "user2@example.com",
        "password": "Password2"
    }
    client.post("/register", json=user2_data)
    login2_response = client.post("/token", data={
        "username": user2_data["email"],
        "password": user2_data["password"]
    })
    token2 = login2_response.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # User 2 tries to access User 1's todo
    response = client.get(f"/todos/{todo_id}", headers=headers2)
    assert response.status_code == 404

# Test Priority Validation
def test_todo_priority_values(auth_headers):
    """Test that todos can have priorities from 1 to 5"""
    for priority in range(1, 6):
        todo_data = {
            "title": f"Priority {priority} Todo",
            "description": "Test",
            "priority": priority,
            "isCompleted": False
        }
        response = client.post("/todos", json=todo_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["priority"] == priority

# Test Completion Status
def test_toggle_todo_completion(auth_headers):
    """Test marking todo as complete and incomplete"""
    # Create todo
    todo_data = {
        "title": "Complete Test",
        "description": "Test",
        "priority": 1,
        "isCompleted": False
    }
    create_response = client.post("/todos", json=todo_data, headers=auth_headers)
    todo_id = create_response.json()["id"]

    # Mark as complete
    update_data = {
        **todo_data,
        "isCompleted": True
    }
    response = client.put(f"/todos/{todo_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["isCompleted"] == True

    # Mark as incomplete
    update_data["isCompleted"] = False
    response = client.put(f"/todos/{todo_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["isCompleted"] == False

# Test Batch Operations
def test_create_20_todos_and_validate(auth_headers):
    """Test creating 20 todos in a loop and validating them"""
    created_ids = []

    # Create 20 todos
    for i in range(1, 21):
        todo_data = {
            "title": f"TODO {i}",
            "description": f"Description for TODO {i}",
            "priority": i if i <= 5 else (i % 5) + 1,
            "isCompleted": False
        }
        response = client.post("/todos", json=todo_data, headers=auth_headers)
        assert response.status_code == 200
        created_ids.append(response.json()["id"])

    # Get all todos and validate
    response = client.get("/todos", headers=auth_headers)
    assert response.status_code == 200
    todos = response.json()

    # Validate count
    assert len([t for t in todos if t["id"] in created_ids]) == 20

    # Validate titles
    titles = [t["title"] for t in todos if t["id"] in created_ids]
    for i in range(1, 21):
        assert f"TODO {i}" in titles

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
