const API_URL = 'http://127.0.0.1:8000';

// Проверка токена и управление кнопкой логина/логаута
document.addEventListener('DOMContentLoaded', () => {
    const authButton = document.getElementById('authButton');
    const token = localStorage.getItem('accessToken');

    if (token) {
        // Пользователь залогинен, показываем "Log Out"
        authButton.textContent = 'Log Out';
        authButton.href = '#';
        authButton.addEventListener('click', async () => {
            try {
                await logout();
            } catch (error) {
                console.error('Logout failed', error);
            }
        });

        // Проверяем роль пользователя и подгружаем интерфейс
        fetchUserProfile();
    } else {
        authButton.textContent = 'Log In';
        authButton.href = 'html/auth.html';
    }

    fetchGoods();
});

// Logout функция
async function logout() {
    const token = localStorage.getItem('accessToken');
    const response = await fetch(`${API_URL}/auth/logout`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        localStorage.removeItem('accessToken');
        console.log('Logged out');
        window.location.reload();
    } else {
        console.log('Logout failed');
    }
}

// Проверяем профиль пользователя и роль
async function fetchUserProfile() {
    const token = localStorage.getItem('accessToken');
    if (!token) return;

    try {
        const response = await fetch(`${API_URL}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const userData = await response.json();

            // Проверяем роль пользователя
            if (userData.roleid) {
                const roleResponse = await fetch(`${API_URL}/roles/${userData.roleid}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });

                if (roleResponse.ok) {
                    const roleData = await roleResponse.json();
                    if (roleData.name === 'admin') {
                        displayAdminMenu();
                    }
                }
            }
        }
    } catch (error) {
        console.error('Failed to fetch user profile', error);
    }
}

// Функция для отображения административных кнопок
function displayAdminMenu() {
    const ordersButton = document.getElementById('ordersButton');
    const logsButton = document.getElementById('logsButton');
    const usersButton = document.getElementById('usersButton');
    const dataButton = document.createElement('li'); // Создаем кнопку "Data"

    // Настройка кнопки Data
    dataButton.className = 'nav-item';
    dataButton.innerHTML = `
        <a href="../html/data.html" class="nav-link btn btn-outline-light ml-3">Data</a>
    `;

    const nav = document.querySelector('.nav');
    nav.appendChild(dataButton);

    // Показ админских кнопок
    ordersButton.style.display = 'block';
    logsButton.style.display = 'block';
    usersButton.style.display = 'block';
    dataButton.style.display = 'block';
}



// Получаем все товары
async function fetchGoods() {
    try {
        const response = await fetch(`${API_URL}/goods/`);
        const goods = await response.json();
        displayGoods(goods);

        // Получаем данные для выпадающих списков
        fetchAnimals();
        fetchFirms();
        fetchCategories();
    } catch (error) {
        console.error('Error loading goods:', error);
        document.getElementById('content').innerHTML = '<p>Failed to load goods. Please try again later.</p>';
    }
}

// Получаем животных
async function fetchAnimals() {
    try {
        const response = await fetch(`${API_URL}/animals/`);
        const animals = await response.json();
        populateDropdown('animalsDropdown', animals, 'animalid', 'type');
    } catch (error) {
        console.error('Error fetching animals:', error);
    }
}

// Получаем фирмы
async function fetchFirms() {
    try {
        const response = await fetch(`${API_URL}/firms/`);
        const firms = await response.json();
        populateDropdown('firmsDropdown', firms, 'firmid', 'naming');
    } catch (error) {
        console.error('Error fetching firms:', error);
    }
}

// Получаем категории
async function fetchCategories() {
    try {
        const response = await fetch(`${API_URL}/categories/`);
        const categories = await response.json();
        populateDropdown('categoriesDropdown', categories, 'categoryofgoodid', 'title');
    } catch (error) {
        console.error('Error fetching categories:', error);
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
            <div class="card" style="cursor: pointer;">
                <img src="${good.imageurl}" class="card-img-top" alt="${good.title}">
                <div class="card-body text-center">
                    <h5 class="card-title">${good.title}</h5>
                    <p class="card-text">$${good.price}</p>
                    <button class="btn btn-primary add-to-cart" style="background-color: #8395a6; border: #8395a6" data-id="${good.id}">Add to Cart</button>
                </div>
            </div>
        `;

        // Добавляем обработчик клика на карточку
        div.querySelector('.card').addEventListener('click', () => {
            window.location.href = `../html/product.html?id=${good.id}`;
        });

        // Добавляем карточку на страницу
        content.appendChild(div);
    });

    // Обработчики для кнопок "Add to Cart"
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', async (e) => {
            e.stopPropagation(); // Останавливаем событие клика на карточке
            const productId = button.dataset.id;
            const token = localStorage.getItem('accessToken');

            if (!token) {
                alert('You must log in first.');
                window.location.href = '../html/auth.html';
                return;
            }

            let cartId = localStorage.getItem('cartid');

            // Если корзина отсутствует, запросим её
            if (!cartId) {
                try {
                    const userResponse = await fetch(`${API_URL}/auth/me`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });

                    if (userResponse.ok) {
                        const userData = await userResponse.json();
                        const cartResponse = await fetch(`${API_URL}/carts/${userData.id}`, {
                            headers: { 'Authorization': `Bearer ${token}` }
                        });

                        if (cartResponse.ok) {
                            const cartData = await cartResponse.json();
                            cartId = cartData.id;
                            localStorage.setItem('cartid', cartId);
                        } else {
                            console.log('Could not fetch cart.');
                            return;
                        }
                    } else {
                        console.log('Could not fetch user profile.');
                        return;
                    }
                } catch (error) {
                    console.error('Error fetching cart ID:', error);
                    console.log('An unexpected error occurred');
                    return;
                }
            }

            // Отправляем товар в корзину
            try {
                const response = await fetch(`${API_URL}/carts/add_good`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ cart_id: cartId, good_id: productId }),
                });

                if (response.ok) {
                    console.log('Product added to cart successfully!');
                } else {
                    const errorData = await response.json();
                    console.log(`Failed to add product to cart: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error adding product to cart:', error);
                console.log('An unexpected error occurred');
            }
        });
    });
}


// Фильтрация товаров по выбранному критерию
async function filterGoods(filterType, filterValue) {
    try {
        const response = await fetch(`${API_URL}/goods/`);
        const goods = await response.json();
        const filteredGoods = goods.filter(good => good[filterType] === filterValue);
        displayGoods(filteredGoods);
    } catch (error) {
        console.error('Filter error:', error);
    }
}

// Заполняем выпадающее меню
function populateDropdown(dropdownId, items, filterType, displayField) {
    const dropdown = document.getElementById(dropdownId);
    dropdown.innerHTML = '';

    items.forEach(item => {
        const a = document.createElement('a');
        a.className = 'dropdown-item';
        a.href = '#';
        a.textContent = item[displayField] || "Unknown";
        a.addEventListener('click', () => filterGoods(filterType, item.id));
        dropdown.appendChild(a);
    });
}
