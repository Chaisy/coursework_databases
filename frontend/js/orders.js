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

// Загрузка всех заказов при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    if (!isLoggedIn()) {
        console.log('You must log in to view orders');
        window.location.href = 'html/auth.html'; // Перенаправляем на страницу логина
    } else {
        await fetchOrders();
    }
});

// Функция для загрузки всех заказов
async function fetchOrders() {
    try {
        const response = await fetch(`${API_URL}/orders`, {
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });

        if (response.ok) {
            const orders = await response.json();
            populateOrdersTable(orders);
        } else {
            console.log('Failed to load orders');
        }
    } catch (error) {
        console.error('Error while fetching orders', error);
        console.log('An error occurred while fetching orders');
    }
}

// Отображаем заказы в таблице
function populateOrdersTable(orders) {
    const tableBody = document.querySelector("#ordersTable tbody");
    tableBody.innerHTML = ''; // Очищаем таблицу перед новой загрузкой

    if (orders.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center">No orders found</td>
            </tr>
        `;
        return;
    }

    orders.forEach(order => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${order.id}</td>
            <td>${order.userId}</td>
            <td>${order.goods.join(', ')}</td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="deleteOrder('${order.id}')">Remove</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Функция для удаления заказа
async function deleteOrder(orderId) {
    if (!confirm('Are you sure you want to delete this order?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/orders/${orderId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });

        if (response.ok) {
            console.log('Order deleted successfully');
            await fetchOrders(); // Перезагружаем список заказов
        } else {
            const error = await response.json();
            console.log(`Failed to delete order: ${error.detail || 'Unknown error'}`);
        }
    } catch (error) {
        console.error('Error while deleting order', error);
        console.log('An error occurred while deleting the order');
    }
}
