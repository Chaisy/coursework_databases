const API_URL = 'http://127.0.0.1:8000';

// Получение токена из localStorage
function getToken() {
    return localStorage.getItem('accessToken');
}

// Проверка наличия токена
function isLoggedIn() {
    return !!getToken();
}

// Загрузка пользователей при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    if (!isLoggedIn()) {
        console.log('You must log in to view users');
        window.location.href = 'auth.html';
    } else {
        await fetchUsers();
    }
});

// Загрузка всех пользователей
async function fetchUsers() {
    try {
        const response = await fetch(`${API_URL}/users`, {
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });

        if (response.ok) {
            const users = await response.json();
            populateUsersTable(users);
        } else {
            console.log('Failed to load users');
        }
    } catch (error) {
        console.error('Error while fetching users', error);
    }
}

// Отображение пользователей в таблице
function populateUsersTable(users) {
    console.log(users)
    const tableBody = document.querySelector("#usersTable tbody");
    tableBody.innerHTML = '';

    if (users.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center">No users found</td>
            </tr>
        `;
        return;
    }

    users.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.id}</td>
            <td>${user.login}</td>
            <td>${user.name}</td>
            <td>${user.roleid || 'N/A'}</td>
            <td>${user.couponid || 'N/A'}</td>
            <td>${user.banned ? 'Yes' : 'No'}</td>
            <td>
                <button class="btn btn-${user.banned ? 'success' : 'danger'} btn-sm" 
                        onclick="toggleBan('${user.id}', ${user.banned})">
                    ${user.banned ? 'Unban' : 'Ban'}
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Функция для бана/разбана пользователя
async function toggleBan(userId, currentStatus) {
    try {
        const response = await fetch(`${API_URL}/users/${userId}/ban`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });

        if (response.ok) {
            console.log(`User ${currentStatus ? 'unbanned' : 'banned'} successfully`);
            await fetchUsers(); // Перезагружаем таблицу
        } else {
            const error = await response.json();
            console.log(`Failed to update user status: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error toggling user ban', error);
    }
}
