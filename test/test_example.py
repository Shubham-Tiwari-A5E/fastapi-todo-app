def test_equal_or_not_equal():
    assert 2 == 2
    assert 3 != 1

def test_is_instance():
    assert isinstance("This is string", str)

import requests

def test_add_todos():
    base_url = "http://127.0.0.1:8000"

    # Register user (if not exists)
    register_data = {
        "name": "Test User",
        "email": "sstt291094@gmail.com",
        "password": "TestPassword@@1111"
    }
    response = requests.post(f"{base_url}/register", json=register_data)
    # Assume it succeeds or already exists

    # Login to get token
    login_data = {
        "username": "sstt291094@gmail.com",
        "password": "TestPassword@@1111"
    }
    response = requests.post(f"{base_url}/token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Add 20 todos
    for i in range(1, 21):
        todo_data = {
            "title": f"TODO {i}",
            "description": f"Description for TODO {i}",
            "priority": i,
            "isCompleted": False
        }
        response = requests.post(f"{base_url}/todos", json=todo_data, headers=headers)
        assert response.status_code == 200

    # Get todos and validate
    response = requests.get(f"{base_url}/todos", headers=headers)
    assert response.status_code == 200
    todos = response.json()

    # Check that at least 20 todos are there
    assert len(todos) >= 20
    actual_titles = [t["title"] for t in todos]
    expected_titles = [f"TODO {i}" for i in range(1, 21)]
    for title in expected_titles:
        assert title in actual_titles

    # Check priorities
    actual_priorities = [t["priority"] for t in todos]
    expected_priorities = list(range(1, 21))
    for pri in expected_priorities:
        assert pri in actual_priorities
