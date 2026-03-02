import pytest
import sys
import os
import time

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
        "name": "Completed Test User",
        "email": "completedtest@example.com",
        "password": "TestPassword123"
    }
    response = client.post("/register", json=user_data)
    return user_data

@pytest.fixture
def auth_headers(test_user):
    """Get authorization headers"""
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_completed_at_set_when_marking_complete(auth_headers):
    """Test that completed_at is set when marking todo as complete"""
    # Create a todo
    todo_data = {
        "title": "Test Completion",
        "description": "Test",
        "priority": 1,
        "isCompleted": False
    }
    create_response = client.post("/todos", json=todo_data, headers=auth_headers)
    assert create_response.status_code == 200
    todo = create_response.json()
    todo_id = todo["id"]

    # Verify completed_at is None
    assert todo.get("completed_at") is None

    # Mark as complete
    update_data = {
        "title": "Test Completion",
        "description": "Test",
        "priority": 1,
        "isCompleted": True
    }
    update_response = client.put(f"/todos/{todo_id}", json=update_data, headers=auth_headers)
    assert update_response.status_code == 200
    updated_todo = update_response.json()

    # Verify completed_at is now set
    assert updated_todo["isCompleted"] == True
    assert updated_todo.get("completed_at") is not None

def test_completed_at_cleared_when_marking_incomplete(auth_headers):
    """Test that completed_at is cleared when marking todo as incomplete"""
    # Create a completed todo
    todo_data = {
        "title": "Test Uncomplete",
        "description": "Test",
        "priority": 1,
        "isCompleted": True
    }
    create_response = client.post("/todos", json=todo_data, headers=auth_headers)
    assert create_response.status_code == 200
    todo_id = create_response.json()["id"]

    # Mark as incomplete
    update_data = {
        "title": "Test Uncomplete",
        "description": "Test",
        "priority": 1,
        "isCompleted": False
    }
    update_response = client.put(f"/todos/{todo_id}", json=update_data, headers=auth_headers)
    assert update_response.status_code == 200
    updated_todo = update_response.json()

    # Verify completed_at is cleared
    assert updated_todo["isCompleted"] == False
    assert updated_todo.get("completed_at") is None

def test_create_already_completed_todo(auth_headers):
    """Test creating a todo that's already marked as completed"""
    todo_data = {
        "title": "Already Completed",
        "description": "Test",
        "priority": 1,
        "isCompleted": True
    }
    response = client.post("/todos", json=todo_data, headers=auth_headers)
    assert response.status_code == 200
    todo = response.json()

    # Should have completed_at set
    assert todo["isCompleted"] == True
    assert todo.get("completed_at") is not None

def test_multiple_completion_toggles(auth_headers):
    """Test toggling completion status multiple times"""
    # Create todo
    todo_data = {
        "title": "Toggle Test",
        "description": "Test",
        "priority": 1,
        "isCompleted": False
    }
    create_response = client.post("/todos", json=todo_data, headers=auth_headers)
    todo_id = create_response.json()["id"]

    # Mark complete
    update_data = {**todo_data, "isCompleted": True}
    response1 = client.put(f"/todos/{todo_id}", json=update_data, headers=auth_headers)
    first_completed_at = response1.json().get("completed_at")
    assert first_completed_at is not None

    time.sleep(0.2)  # Increased delay to ensure different timestamps

    # Mark incomplete
    update_data["isCompleted"] = False
    response2 = client.put(f"/todos/{todo_id}", json=update_data, headers=auth_headers)
    assert response2.json().get("completed_at") is None

    time.sleep(0.2)  # Increased delay to ensure different timestamps

    # Mark complete again
    update_data["isCompleted"] = True
    response3 = client.put(f"/todos/{todo_id}", json=update_data, headers=auth_headers)
    second_completed_at = response3.json().get("completed_at")
    assert second_completed_at is not None

    # The second completion should have a different (later) timestamp
    # Convert to strings for comparison if they're datetime objects
    first_str = str(first_completed_at)
    second_str = str(second_completed_at)
    assert first_str != second_str, f"Timestamps should be different: {first_str} vs {second_str}"

def test_completed_todos_in_filter(auth_headers):
    """Test that completed todos can be filtered and have completed_at"""
    # Create mix of todos
    todos = [
        {"title": "Active 1", "priority": 1, "isCompleted": False},
        {"title": "Completed 1", "priority": 2, "isCompleted": True},
        {"title": "Completed 2", "priority": 3, "isCompleted": True},
    ]

    for todo in todos:
        client.post("/todos", json={**todo, "description": "Test"}, headers=auth_headers)

    # Get all todos
    response = client.get("/todos", headers=auth_headers)
    all_todos = response.json()

    # Filter completed todos
    completed_todos = [t for t in all_todos if t["isCompleted"] and "Completed" in t["title"]]

    # All completed todos should have completed_at
    for todo in completed_todos:
        assert todo.get("completed_at") is not None

def test_completed_at_format(auth_headers):
    """Test that completed_at is in valid datetime format"""
    # Create and complete a todo
    todo_data = {
        "title": "Format Test",
        "description": "Test",
        "priority": 1,
        "isCompleted": True
    }
    response = client.post("/todos", json=todo_data, headers=auth_headers)
    todo = response.json()

    completed_at = todo.get("completed_at")
    assert completed_at is not None

    # Verify it's a valid datetime string (basic check)
    from datetime import datetime
    try:
        # Try to parse the datetime string
        if 'T' in completed_at:
            datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
        else:
            datetime.strptime(completed_at, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        pytest.fail(f"completed_at is not in valid datetime format: {completed_at}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
