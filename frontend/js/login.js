const API_URL = 'http://127.0.0.1:8000/auth';

// Обработка формы логина
document.getElementById('loginForm')?.addEventListener('submit', async (event) => {
    event.preventDefault(); // Отменяем стандартное поведение формы

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            const error = await response.json();
            console.log(error.detail || 'Login failed');
            return;
        }

        const data = await response.json();
        localStorage.setItem('accessToken', data.access_token); // Сохраняем токен в localStorage
        console.log('Login successful!');
        window.location.href = 'http://127.0.0.1:8080/'; // Перенаправляем на главную страницу
    } catch (error) {
        console.error('Error during login:', error);
        console.log('An error occurred. Please try again later.');
    }
});

// Обработка формы регистрации
document.getElementById('registerForm')?.addEventListener('submit', async (event) => {
    event.preventDefault(); // Отменяем стандартное поведение формы

    const name = document.getElementById('name').value;
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, login, password })
        });

        if (!response.ok) {
            const error = await response.json();
            console.log(error.detail || 'Registration failed');
            return;
        }

        console.log('Registration successful! You can now log in.');
        window.location.href = 'auth.html'; // Перенаправляем на страницу логина
    } catch (error) {
        console.error('Error during registration:', error);
        console.log('An error occurred. Please try again later.');
    }
});
