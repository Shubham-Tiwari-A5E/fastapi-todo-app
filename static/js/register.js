document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const errorDiv = document.getElementById('error-message');
    const successDiv = document.getElementById('success-message');
    errorDiv.style.display = 'none';
    successDiv.style.display = 'none';

    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            successDiv.textContent = 'Registration successful! Redirecting to login...';
            successDiv.style.display = 'block';

            // Redirect to login after 2 seconds
            setTimeout(() => {
                window.location.href = '/login';
            }, 2000);
        } else {
            errorDiv.textContent = data.detail || 'Registration failed. Please try again.';
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        errorDiv.textContent = 'An error occurred. Please try again.';
        errorDiv.style.display = 'block';
    }
});
