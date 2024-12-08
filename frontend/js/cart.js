const API_URL = 'http://127.0.0.1:8000';

// Функция для получения ID корзины
async function fetchCartId(token) {
    let cartId = localStorage.getItem('cartid');

    if (!cartId) {
        try {
            const userResponse = await fetch(`${API_URL}/auth/me`, {
                headers: { 'Authorization': `Bearer ${token}` },
            });

            if (userResponse.ok) {
                const userData = await userResponse.json();
                localStorage.setItem('userId', userData.id); // Сохраняем ID пользователя
                const cartResponse = await fetch(`${API_URL}/carts/${userData.id}`, {
                    headers: { 'Authorization': `Bearer ${token}` },
                });

                if (cartResponse.ok) {
                    const cartData = await cartResponse.json();
                    cartId = cartData.id;
                    localStorage.setItem('cartid', cartId);
                } else {
                    console.log('Could not fetch cart.');
                    return null;
                }
            } else {
                console.log('Could not fetch user profile.');
                return null;
            }
        } catch (error) {
            console.error('Error fetching cart ID:', error);
            console.log('An unexpected error occurred');
            return null;
        }
    }

    return cartId;
}

// Запрос товаров из корзины
async function fetchCartGoods() {
    const token = localStorage.getItem('accessToken');
    if (!token) {
        console.log('You must log in to view your cart');
        window.location.href = '../html/auth.html';
        return;
    }

    const cartId = await fetchCartId(token);
    if (!cartId) return;

    try {
        const response = await fetch(`${API_URL}/carts/${cartId}/goods`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (response.ok) {
            const goodsIds = await response.json();
            const goodsDetails = await fetchGoodsDetails(goodsIds, token);
            displayGoods(goodsDetails);
        } else {
            console.log('No goods in cart or error fetching goods');
        }
    } catch (error) {
        console.error('Error loading cart goods:', error);
    }
}

// Запрос деталей товаров по их ID
async function fetchGoodsDetails(goodsIds, token) {
    const goodsDetails = [];

    for (const id of goodsIds) {
        try {
            const response = await fetch(`${API_URL}/goods/${id}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const good = await response.json();
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

// Функция для удаления товара из корзины
async function removeGoodFromCart(goodId) {
    const token = localStorage.getItem('accessToken');
    const cartId = localStorage.getItem('cartid');
    if (!token || !cartId) {
        console.log('You need to log in first.');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/carts/remove-good`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({
                cart_id: cartId,
                good_id: goodId,
            }),
        });

        if (response.ok) {
            console.log('Item removed successfully');
            fetchCartGoods(); // Обновляем корзину
        } else {
            const error = await response.json();
            console.log(`Failed to remove item: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error removing item from cart:', error);
        console.log('An error occurred. Please try again later.');
    }
}

// Функция для добавления товара в заказ
async function addGoodToOrder(goodId) {
    const token = localStorage.getItem('accessToken');

    const userId = localStorage.getItem('userId');
    console.log(token)
    console.log(userId)
    if (!token || !userId) {
        console.log('You need to log in first.');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/orders/${userId}/${goodId}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (response.ok) {
            console.log('Item added to order successfully');
            fetchCartGoods(); // Перезагрузка корзины
        } else {
            const error = await response.json();
            console.log(`Failed to add item to order: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error adding item to order:', error);
        console.log('An error occurred. Please try again later.');
    }
}

// Отображение товаров
function displayGoods(goods) {
    const content = document.getElementById('content');
    content.innerHTML = '';

    goods.forEach(good => {
        const div = document.createElement('div');
        div.className = 'col-md-4 mb-4';
        div.innerHTML = `
            <div class="card text-center">
                <img src="${good.imageurl}" class="card-img-top" alt="${good.title}">
                <div class="card-body">
                    <h5 class="card-title">${good.title}</h5>
                    <p class="card-text">$${good.price}</p>
                    <button class="btn btn-danger remove-button" data-good-id="${good.id}">Remove</button>
                    <button class="btn btn-success order-button" data-good-id="${good.id}">Add to Order</button>
                </div>
            </div>
        `;
        content.appendChild(div);
    });

    // Назначаем обработчики кнопкам удаления
    const removeButtons = document.querySelectorAll('.remove-button');
    removeButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            const goodId = e.target.getAttribute('data-good-id');
            await removeGoodFromCart(goodId);
        });
    });

    // Назначаем обработчики кнопкам добавления в заказ
    const orderButtons = document.querySelectorAll('.order-button');
    orderButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            const goodId = e.target.getAttribute('data-good-id');
            await addGoodToOrder(goodId);
        });
    });
}

// Инициализация страницы
document.addEventListener('DOMContentLoaded', () => {
    fetchCartGoods();
});


// See all orders, users
// Ban users
