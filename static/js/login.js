document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const errorDiv = document.getElementById('error-message');
    errorDiv.style.display = 'none';

    const formData = new FormData(e.target);

    try {
        const response = await fetch('/token', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // Store token in localStorage
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('email', formData.get('username'));

            // Redirect to dashboard
            window.location.href = '/dashboard';
        } else {
            errorDiv.textContent = data.detail || 'Login failed. Please check your credentials.';
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        errorDiv.textContent = 'An error occurred. Please try again.';
        errorDiv.style.display = 'block';
    }
});
