const API_URL = 'http://127.0.0.1:8000';

// Получение всех заказов пользователя
async function fetchUserOrders() {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        console.log('You must log in to view your orders');
        window.location.href = '../html/auth.html';
        return;
    }

    try {
        // Получение данных о пользователе
        const userResponse = await fetch(`${API_URL}/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` },
        });

        if (userResponse.ok) {
            const userData = await userResponse.json();
            const userId = userData.id;

            // Получение всех заказов пользователя
            const ordersResponse = await fetch(`${API_URL}/orders/user/${userId}`, {
                headers: { 'Authorization': `Bearer ${token}` },
            });


            if (ordersResponse.ok) {
                const orders = await ordersResponse.json(); // Массив заказов
                const ordersDetails = await fetchOrdersDetails(orders, token); // Детали заказов
                displayOrders(ordersDetails); // Отображение заказов
            } else {
                console.log('Failed to fetch orders');
            }
        } else {
            console.log('Could not fetch user profile');
        }
    } catch (error) {
        console.error('Error fetching user orders:', error);
    }
}

// Получение деталей каждого заказа
async function fetchOrdersDetails(orderIds, token) {
    const ordersDetails = [];

    for (const order of orderIds) {
        try {
            const orderId = order.id; // Извлекаем ID заказа
            const response = await fetch(`${API_URL}/orders/${orderId}`, {
                headers: { 'Authorization': `Bearer ${token}` },
            });

            if (response.ok) {
                const goodsIds = await response.json(); // Получаем список ID товаров
                console.log(goodsIds)
                const goodsDetails = await fetchGoodsDetails(goodsIds, token); // Получаем детали товаров
                ordersDetails.push({ id: orderId, goods: goodsDetails });
            } else {
                console.warn(`Failed to fetch goods for order ID ${orderId}`);
            }
        } catch (error) {
            console.error(`Error fetching goods for order ID ${orderId}:`, error);
        }
    }

    return ordersDetails;
}

// Запрос деталей товаров по их ID
async function fetchGoodsDetails(goodsIds, token) {
    const goodsDetails = [];

    for (const id of goodsIds) {
        try {
            const response = await fetch(`${API_URL}/goods/${id}`, {
                headers: { 'Authorization': `Bearer ${token}` },
            });

            if (response.ok) {
                const good = await response.json(); // Детали товара
                goodsDetails.push(good);
            } else {
                console.warn(`Failed to fetch details for good ID ${id}`);
            }
        } catch (error) {
            console.error(`Error fetching details for good ID ${id}:`, error);
        }
    }

    return goodsDetails;
}

// Отображение заказов и их товаров
function displayOrders(orders) {
    const content = document.getElementById('content');
    content.innerHTML = '';

    orders.forEach(order => {
        // Карточка заказа
        const orderDiv = document.createElement('div');
        orderDiv.className = 'col-12 mb-4';
        orderDiv.innerHTML = `
            <div class="card">
                <div class="card-header text-center">
                    <h5>Order ID: ${order.id}</h5>
                </div>
                <div class="card-body">
                    <div class="row" id="goods-${order.id}"></div>
                </div>
            </div>
        `;
        content.appendChild(orderDiv);

        // Добавляем товары в карточку заказа
        const goodsContainer = document.getElementById(`goods-${order.id}`);
        order.goods.forEach(good => {
            const goodDiv = document.createElement('div');
            goodDiv.className = 'col-md-4 mb-3';
            goodDiv.innerHTML = `
                <div class="card text-center">
                    <img src="${good.imageurl}" class="card-img-top" alt="${good.title}">
                    <div class="card-body">
                        <h5 class="card-title">${good.title}</h5>
                        <p class="card-text">$${good.price}</p>
                        <button class="btn btn-danger remove-button" data-order-id="${order.id}" data-good-id="${good.id}">
                            Remove
                        </button>
                    </div>
                </div>
            `;
            goodsContainer.appendChild(goodDiv);
        });
    });

    // Добавляем обработчики на кнопки "Remove"
    document.querySelectorAll('.remove-button').forEach(button => {
        button.addEventListener('click', async () => {
            const orderId = button.dataset.orderId;
            const goodId = button.dataset.goodId;
            const token = localStorage.getItem('accessToken');

            try {
                const response = await fetch(`${API_URL}/orders/${orderId}/${goodId}`, {
                    method: 'DELETE',
                    headers: { 'Authorization': `Bearer ${token}` },
                });

                if (response.ok) {
                    console.log('Product removed successfully!');
                    // Обновляем заказы после удаления
                    fetchUserOrders();
                } else {
                    const errorData = await response.json();
                    console.log(`Failed to remove product: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error removing product from order:', error);
                console.log('An unexpected error occurred');
            }
        });
    });
}


// Инициализация страницы
document.addEventListener('DOMContentLoaded', () => {
    fetchUserOrders();
});
