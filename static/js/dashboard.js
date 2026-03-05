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

// Profile Modal functionality
const profileModal = document.getElementById('profileModal');
const profileBtn = document.getElementById('profileBtn');
const cancelProfile = document.getElementById('cancelProfile');

profileBtn.addEventListener('click', async () => {
    await loadProfile();
    profileModal.style.display = 'block';
    document.body.classList.add('modal-open');
});

cancelProfile.addEventListener('click', () => {
    profileModal.style.display = 'none';
    document.body.classList.remove('modal-open');
});

window.addEventListener('click', (e) => {
    if (e.target === profileModal) {
        profileModal.style.display = 'none';
        document.body.classList.remove('modal-open');
    }
});

// Load user profile
async function loadProfile() {
    try {
        const response = await fetch('/profile', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const user = await response.json();
            document.getElementById('profileName').value = user.name;
            document.getElementById('profileEmail').value = user.email;
            document.getElementById('profilePhone').value = user.phone_number || '';
        }
    } catch (error) {
        console.error('Failed to load profile:', error);
    }
}

// Update user profile
document.getElementById('profileForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const profileMessage = document.getElementById('profileMessage');
    profileMessage.style.display = 'none';

    const formData = {
        name: document.getElementById('profileName').value,
        phone_number: document.getElementById('profilePhone').value || null
    };

    try {
        const response = await fetch('/profile', {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            profileMessage.textContent = '✅ Profile updated successfully!';
            profileMessage.style.background = '#d4edda';
            profileMessage.style.color = '#155724';
            profileMessage.style.display = 'block';

            // Update display name
            document.getElementById('userName').textContent = formData.name;

            setTimeout(() => {
                profileModal.style.display = 'none';
                document.body.classList.remove('modal-open');
            }, 1500);
        } else {
            const data = await response.json();
            profileMessage.textContent = '❌ ' + (data.detail || 'Failed to update profile');
            profileMessage.style.background = '#f8d7da';
            profileMessage.style.color = '#721c24';
            profileMessage.style.display = 'block';
        }
    } catch (error) {
        profileMessage.textContent = '❌ An error occurred';
        profileMessage.style.background = '#f8d7da';
        profileMessage.style.color = '#721c24';
        profileMessage.style.display = 'block';
    }
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
            ${todo.task_time ? `<p class="task-time">⏰ Scheduled: ${formatDate(todo.task_time)}</p>` : ''}
            ${todo.task_time && todo.notification_enabled && !todo.isCompleted ? `<p class="notification-status">📱 Reminder enabled (10 min before)</p>` : ''}
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

// Format date for display (without timezone conversion)
function formatDate(dateString) {
    if (!dateString) return 'No date set';

    // Parse the date string directly without timezone conversion
    const parts = dateString.split('T');
    if (!parts[0] || !parts[1]) return dateString;

    const datePart = parts[0].split('-');
    const timePart = parts[1].split(':');

    const year = datePart[0];
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December'];
    const month = monthNames[parseInt(datePart[1]) - 1];
    const day = parseInt(datePart[2]);

    // Convert 24-hour to 12-hour format
    let hour = parseInt(timePart[0]);
    const minute = timePart[1].padStart(2, '0');
    const ampm = hour >= 12 ? 'PM' : 'AM';
    hour = hour % 12 || 12; // Convert 0 to 12

    return `${month} ${day}, ${year} ${hour}:${minute} ${ampm}`;
}

// Modal functionality
const modal = document.getElementById('todoModal');
const addBtn = document.getElementById('addTodoBtn');
const cancelBtn = document.getElementById('cancelBtn');

addBtn.addEventListener('click', () => {
    document.getElementById('modalTitle').textContent = 'Add New Task';
    document.getElementById('todoForm').reset();
    document.getElementById('todoId').value = '';
    
    // Hide completed checkbox for new tasks
    document.getElementById('completedCheckboxGroup').style.display = 'none';
    
    modal.style.display = 'block';
    document.body.classList.add('modal-open');
});

cancelBtn.addEventListener('click', () => {
    modal.style.display = 'none';
    document.body.classList.remove('modal-open');
});

window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
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

        // Set task time if exists
        if (todo.task_time) {
            // Parse the datetime and format for datetime-local input
            // Take the first 16 characters (YYYY-MM-DDTHH:MM) without timezone conversion
            const taskTimeStr = todo.task_time.substring(0, 16);
            document.getElementById('taskTime').value = taskTimeStr;
        } else {
            document.getElementById('taskTime').value = '';
        }

        document.getElementById('notificationEnabled').checked = todo.notification_enabled !== false;

        // Show completed checkbox for editing
        document.getElementById('completedCheckboxGroup').style.display = 'block';

        modal.style.display = 'block';
        document.body.classList.add('modal-open');
    } catch (error) {
        alert('Failed to load task details');
    }
}

// Submit todo form
document.getElementById('todoForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const todoId = document.getElementById('todoId').value;
    const taskTimeValue = document.getElementById('taskTime').value;

    // Convert local time to ISO format without changing the actual time
    // This treats the selected time as the desired time (not as local time to convert to UTC)
    let taskTimeISO = null;
    if (taskTimeValue) {
        // Parse as local time and keep it as-is
        const [datePart, timePart] = taskTimeValue.split('T');
        taskTimeISO = `${datePart}T${timePart}:00`;
    }

    const formData = {
        title: document.getElementById('todoTitle').value,
        description: document.getElementById('todoDescription').value || null,
        priority: parseInt(document.getElementById('todoPriority').value),
        isCompleted: document.getElementById('todoCompleted').checked,
        task_time: taskTimeISO,
        notification_enabled: document.getElementById('notificationEnabled').checked
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
            document.body.classList.remove('modal-open');
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
