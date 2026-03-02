// Check if user is logged in
const token = localStorage.getItem('token');
const email = localStorage.getItem('email');

if (!token) {
    window.location.href = '/login';
}

// Set user name
document.getElementById('userName').textContent = email || 'User';

// Logout functionality
document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('token');
    localStorage.removeItem('email');
    window.location.href = '/';
});

// Filter state
let currentFilter = 'all';
let allTodos = [];

// Filter button functionality
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Update active state
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Set current filter
        currentFilter = btn.dataset.filter;

        // Re-display todos with filter
        displayTodos(allTodos);
    });
});

// Load todos
async function loadTodos() {
    try {
        const response = await fetch('/todos', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
            return;
        }

        const todos = await response.json();
        allTodos = todos; // Store all todos
        displayTodos(todos);
        updateStats(todos);
    } catch (error) {
        console.error('Error loading todos:', error);
        document.getElementById('todosContainer').innerHTML = '<p class="error-message">Failed to load tasks.</p>';
    }
}

// Display todos with filtering
function displayTodos(todos) {
    const container = document.getElementById('todosContainer');

    // Apply filter
    let filteredTodos = todos;
    if (currentFilter === 'active') {
        filteredTodos = todos.filter(t => !t.isCompleted);
    } else if (currentFilter === 'completed') {
        filteredTodos = todos.filter(t => t.isCompleted);
    }

    if (filteredTodos.length === 0) {
        const message = currentFilter === 'all'
            ? 'No tasks yet. Click "Add Task" to create one!'
            : currentFilter === 'active'
            ? 'No active tasks. Great job!'
            : 'No completed tasks yet.';
        container.innerHTML = `<p class="loading">${message}</p>`;
        return;
    }

    container.innerHTML = filteredTodos.map(todo => `
        <div class="todo-item ${todo.isCompleted ? 'completed' : ''}">
            <div class="todo-header">
                <div>
                    <span class="todo-title">${escapeHtml(todo.title)}</span>
                    <span class="todo-priority priority-${todo.priority}">Priority ${todo.priority}</span>
                </div>
                ${todo.isCompleted ? '<div class="completed-badge">✓ Completed</div>' : ''}
            </div>
            ${todo.description ? `<p class="todo-description">${escapeHtml(todo.description)}</p>` : ''}
            ${todo.isCompleted && todo.completed_at ? `<p class="completed-date">Completed on: ${formatDate(todo.completed_at)}</p>` : ''}
            <div class="todo-actions">
                ${!todo.isCompleted ? `
                    <button class="btn btn-primary" onclick="editTodo('${todo.id}')">Edit</button>
                    <button class="btn btn-primary" onclick="toggleTodo('${todo.id}', true)">Mark Complete</button>
                    <button class="btn btn-danger" onclick="deleteTodo('${todo.id}')">Delete</button>
                ` : `
                    <button class="btn btn-secondary" onclick="toggleTodo('${todo.id}', false)">Mark Incomplete</button>
                `}
            </div>
        </div>
    `).join('');
}

// Update statistics
function updateStats(todos) {
    const total = todos.length;
    const completed = todos.filter(t => t.isCompleted).length;
    const pending = total - completed;

    document.getElementById('totalTasks').textContent = total;
    document.getElementById('completedTasks').textContent = completed;
    document.getElementById('pendingTasks').textContent = pending;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return date.toLocaleDateString('en-US', options);
}

// Modal functionality
const modal = document.getElementById('todoModal');
const addBtn = document.getElementById('addTodoBtn');
const closeBtn = document.querySelector('.close');
const cancelBtn = document.getElementById('cancelBtn');

addBtn.addEventListener('click', () => {
    document.getElementById('modalTitle').textContent = 'Add New Task';
    document.getElementById('todoForm').reset();
    document.getElementById('todoId').value = '';
    modal.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

cancelBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

// Edit todo
async function editTodo(id) {
    try {
        const response = await fetch(`/todos/${id}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const todo = await response.json();

        document.getElementById('modalTitle').textContent = 'Edit Task';
        document.getElementById('todoId').value = todo.id;
        document.getElementById('todoTitle').value = todo.title;
        document.getElementById('todoDescription').value = todo.description || '';
        document.getElementById('todoPriority').value = todo.priority;
        document.getElementById('todoCompleted').checked = todo.isCompleted;

        modal.style.display = 'block';
    } catch (error) {
        alert('Failed to load task details');
    }
}

// Submit todo form
document.getElementById('todoForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const todoId = document.getElementById('todoId').value;
    const formData = {
        title: document.getElementById('todoTitle').value,
        description: document.getElementById('todoDescription').value || null,
        priority: parseInt(document.getElementById('todoPriority').value),
        isCompleted: document.getElementById('todoCompleted').checked
    };

    try {
        const url = todoId ? `/todos/${todoId}` : '/todos';
        const method = todoId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            modal.style.display = 'none';
            // Reload todos to show the new one at the top
            await loadTodos();
        } else {
            alert('Failed to save task');
        }
    } catch (error) {
        alert('An error occurred while saving the task');
    }
});

// Toggle todo completion
async function toggleTodo(id, isCompleted) {
    try {
        const response = await fetch(`/todos/${id}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const todo = await response.json();
        todo.isCompleted = isCompleted;

        const updateResponse = await fetch(`/todos/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(todo)
        });

        if (updateResponse.ok) {
            loadTodos();
        }
    } catch (error) {
        alert('Failed to update task');
    }
}

// Delete todo
async function deleteTodo(id) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }

    try {
        const response = await fetch(`/todos/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            loadTodos();
        } else {
            alert('Failed to delete task');
        }
    } catch (error) {
        alert('An error occurred while deleting the task');
    }
}

// Load todos on page load
loadTodos();
