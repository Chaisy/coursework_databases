const API_URL = 'http://127.0.0.1:8000/auth';

// Проверяем токен и загружаем профиль пользователя
document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        console.log('You must log in first.');
        window.location.href = 'html/auth.html';
    }

    try {
        const response = await fetch(`${API_URL}/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const userData = await response.json();
            renderUserProfile(userData);
        } else {
            console.log('Failed to load profile');
        }
    } catch (error) {
        console.error('Error loading profile data:', error);
        console.log('An unexpected error occurred');
    }

    // Обработчик выхода из профиля
    const logoutButton = document.getElementById('logout');
    logoutButton.addEventListener('click', async () => {
        try {
            const logoutResponse = await fetch(`${API_URL}/logout`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (logoutResponse.ok) {
                localStorage.removeItem('accessToken');
                console.log('Successfully logged out');
                window.location.href = 'auth.html';
            } else {
                console.log('Logout failed');
            }
        } catch (error) {
            console.error('Error during logout', error);
            console.log('Logout failed');
        }
    });
});

// Функция для рендеринга данных пользователя
function renderUserProfile(user) {
    document.getElementById('userId').textContent = user.id || 'Not provided';
    document.getElementById('userLogin').textContent = user.login || 'Not provided';
    document.getElementById('userName').textContent = user.name || 'Not provided';
    document.getElementById('userRoleId').textContent = user.roleid || 'Not provided';
    document.getElementById('userCouponId').textContent = user.couponId || 'Not provided';
    document.getElementById('userBanned').textContent = user.banned ? 'Yes' : 'No';
}
document.getElementById('editProfile').addEventListener('click', () => {
    window.location.href = '../html/edit_profile.html';
});
