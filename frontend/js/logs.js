const API_URL = 'http://127.0.0.1:8000';

// Получение токена из localStorage
function getToken() {
    return localStorage.getItem('accessToken');
}

// Проверяем наличие токена
function isLoggedIn() {
    const token = getToken();
    return !!token;
}

// Загрузка всех логов при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    if (!isLoggedIn()) {
        console.log('You must log in to view logs');
        window.location.href = 'html/auth.html'; // Перенаправляем на страницу логина
    } else {
        await fetchLogs();
        await loadUserFilter();
    }
});

// Функция для загрузки всех логов
async function fetchLogs(userId = "") {
    try {
        let url = `${API_URL}/logs`;
        if (userId) {
            url = `${API_URL}/logs/${userId}`;
        }

        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });

        if (response.ok) {
            const logs = await response.json();
            populateLogsTable(logs);
        } else {
            console.log('Failed to load logs');
        }
    } catch (error) {
        console.error('Error while fetching logs', error);
        console.log('An error occurred while fetching logs');
    }
}

// Отображаем логи в таблице
function populateLogsTable(logs) {
    const tableBody = document.querySelector("#logsTable tbody");
    tableBody.innerHTML = ''; // Очищаем таблицу перед новой загрузкой

    if (logs.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center">No logs found</td>
            </tr>
        `;
        return;
    }

    logs.forEach(log => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${log.id || 'Unknown'}</td>
            <td>${log.role}</td>
            <td>${log.action}</td>
            <td>${log.result}</td>
            <td>${new Date(log.timestamp).toLocaleString()}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Загрузить пользователей в выпадающий фильтр
async function loadUserFilter() {
    try {
        const response = await fetch(`${API_URL}/users`, {
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });

        if (response.ok) {
            const users = await response.json();
            const userFilter = document.getElementById('userFilter');

            users.forEach(user => {
                const option = document.createElement('option');
                option.value = user.id;
                option.textContent = user.name || user.id;
                userFilter.appendChild(option);
            });
        } else {
            console.error('Error loading users for filter');
        }
    } catch (error) {
        console.error('Error during loading user filter data', error);
    }
}

// Фильтрация логов по пользователю
function filterLogs() {
    const userId = document.getElementById('userFilter').value;
    fetchLogs(userId);
}
