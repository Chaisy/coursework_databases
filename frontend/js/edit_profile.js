const API_URL = 'http://127.0.0.1:8000/auth';

// Загружаем текущие данные пользователя для формы
document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        console.log('You must log in first.');
        window.location.href = 'auth.html';
    }

    try {
        const response = await fetch(`${API_URL}/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const userData = await response.json();
            document.getElementById('userName').value = userData.name || '';
            document.getElementById('userLogin').value = userData.login || '';
        } else {
            console.log('Failed to load user data');
        }
    } catch (error) {
        console.error('Error loading user data:', error);
        console.log('An unexpected error occurred');
    }

    // Обработчик сохранения изменений
    document.getElementById('editProfileForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const updatedData = {
            name: document.getElementById('userName').value,
            login: document.getElementById('userLogin').value,
        };
        console.log('Sending updated data:', updatedData);

        try {
            const response = await fetch(`${API_URL}/me`, {
                method: 'PATCH',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(updatedData),
            });

            if (response.ok) {
                console.log('Profile updated successfully');
                window.location.href = '../html/my_profile.html';
            } else {
                const errorData = await response.json();
                console.log(`Error updating profile: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error updating profile:', error);
            console.log('An unexpected error occurred');
        }
    });

    // Обработчик отмены редактирования
    document.getElementById('cancelEdit').addEventListener('click', () => {
        window.location.href = '../html/my_profile.html';
    });
});
