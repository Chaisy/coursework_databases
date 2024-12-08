const API_URL = 'http://127.0.0.1:8000'; // Базовый URL API
const token = localStorage.getItem('accessToken');
// Токен из LocalStorage

if (!token) {
    console.log("Unauthorized access. Please log in.");
    window.location.href = "auth.html";
}

// Настройка заголовков авторизации
const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
};

// Функция для отображения сообщений об ошибке
function showError(message) {
    console.log(message);
}

// Универсальная функция для удаления элемента
async function deleteItem(endpoint, id, listId) {
    try {
        const response = await fetch(`${API_URL}/${endpoint}/${id}`, {
            method: 'DELETE',
            headers,
        });

        if (response.ok) {
            document.getElementById(listId).removeChild(document.getElementById(id));
        } else {
            const errorData = await response.json();
            showError(errorData.detail || "Failed to delete item.");
        }
    } catch (error) {
        console.error(error);
        showError("An error occurred.");
    }
}

// Универсальная функция для добавления элемента
async function addItem(endpoint, payload, listId, displayField) {
    try {
        const response = await fetch(`${API_URL}/${endpoint}`, {
            method: 'POST',
            headers,
            body: JSON.stringify(payload),
        });

        if (response.ok) {
            const newItem = await response.json();
            const list = document.getElementById(listId);
            const li = document.createElement('li');
            li.className = "list-group-item d-flex justify-content-between align-items-center";
            li.id = newItem.id;
            li.innerHTML = `
                ${newItem[displayField]}
                <button class="btn btn-danger btn-sm">Delete</button>
            `;
            li.querySelector('button').addEventListener('click', () => deleteItem(endpoint, newItem.id, listId));
            list.appendChild(li);
        } else {
            const errorData = await response.json();
            showError(errorData.detail || "Failed to add item.");
        }
    } catch (error) {
        console.error(error);
        showError("An error occurred.");
    }
}

// Загрузка элементов с сервера
async function loadItems(endpoint, listId, displayField) {
    try {
        const response = await fetch(`${API_URL}/${endpoint}`, { headers });
        if (response.ok) {
            const items = await response.json();
            const list = document.getElementById(listId);
            list.innerHTML = '';
            items.forEach(item => {
                const li = document.createElement('li');
                li.className = "list-group-item d-flex justify-content-between align-items-center";
                li.id = item.id;
                li.innerHTML = `
                    ${item[displayField]}
                    <button class="btn btn-danger btn-sm">Delete</button>
                `;
                li.querySelector('button').addEventListener('click', () => deleteItem(endpoint, item.id, listId));
                list.appendChild(li);
            });
        } else {
            const errorData = await response.json();
            showError(errorData.detail || "Failed to load items.");
        }
    } catch (error) {
        console.error(error);
        showError("An error occurred.");
    }
}

// Обработчики форм
document.getElementById('addFirmForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('firmNameInput').value.trim();
    if (name) {
        addItem('firms', { naming: name }, 'firmsList', 'naming');
        document.getElementById('firmNameInput').value = '';
    }
});

document.getElementById('addCategoryForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('categoryNameInput').value.trim();
    if (name) {
        addItem('categories', { title: name }, 'categoriesList', 'title');
        document.getElementById('categoryNameInput').value = '';
    }
});

document.getElementById('addAnimalForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const type = document.getElementById('animalTypeInput').value.trim();
    if (type) {
        addItem('animals', { type: type }, 'animalsList', 'type');
        document.getElementById('animalTypeInput').value = '';
    }
});

// Загрузка данных при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    loadItems('firms', 'firmsList', 'naming');
    loadItems('categories', 'categoriesList', 'title');
    loadItems('animals', 'animalsList', 'type');
      loadDropdowns(); // Подгрузка данных в выпадающие списки
  loadGoods();
});

function showError(message) {
    alert(message);
}
// Функция создания товара
async function createGood() {
    const title = document.getElementById('goodTitleInput').value.trim();
    const firmId = document.getElementById('firmIdInput').value.trim();
    const categoryId = document.getElementById('categoryIdInput').value.trim();
    const animalId = document.getElementById('animalIdInput').value.trim();
    const price = parseFloat(document.getElementById('goodPriceInput').value.trim());
    const imageURL = document.getElementById('goodImageURLInput').value.trim();

    if (!title || !firmId || !categoryId || !animalId || isNaN(price) || !imageURL) {
        showError("All fields are required and must be valid.");
        return;
    }

    const payload = {
        title,
        firmid: firmId,
        categoryofgoodid: categoryId,
        animalid: animalId,
        price,
        imageurl: imageURL,
    };

    try {
        const response = await fetch(`${API_URL}/goods`, {
            method: 'POST',
            headers,
            body: JSON.stringify(payload),
        });

        if (response.ok) {
            const data = await response.json();
            console.log(`Good created successfully: ${data.title}`);
            document.getElementById('addGoodForm').reset();
            loadGoods(); // Обновляем список товаров после успешного создания
        } else {
            const errorData = await response.json();
            showError(errorData.detail || "Failed to create good.");
        }
    } catch (error) {
        console.error(error);
        showError("An unexpected error occurred.");
    }
}

// Обработчик кнопки создания товара
document.getElementById('addGoodForm').addEventListener('submit', (e) => {
    e.preventDefault();
    createGood();
});

//------------------------------------------------------------------------

// Загрузка данных о товарах
async function loadGoods() {
    try {
        const response = await fetch(`${API_URL}/goods`, { headers });
        const goodsList = document.getElementById('goodsList');
        goodsList.innerHTML = '';

        if (response.ok) {
            const goods = await response.json();
            goods.forEach(good => {
                const li = document.createElement('li');
                li.className = "list-group-item d-flex justify-content-between align-items-center";
                li.id = good.id;
                li.innerHTML = `
                    ${good.title}
                    <button class="btn btn-secondary btn-sm">Edit</button>
                    <button class="btn btn-danger btn-sm ml-2">Delete</button>
                `;

                // Привязка обработчиков
                li.querySelector('.btn-secondary').addEventListener('click', () => populateEditForm(good));
                li.querySelector('.btn-danger').addEventListener('click', () => deleteGood(good.id));

                goodsList.appendChild(li);
            });
        } else {
            showError("Failed to load goods.");
        }
    } catch (error) {
        console.error(error);
        showError("An error occurred while loading goods.");
    }
}

// Функция для заполнения формы редактирования
function populateEditForm(good) {
    document.getElementById('editGoodTitleInput').value = good.title || '';
    document.getElementById('editFirmIdInput').value = good.firmId || '';
    document.getElementById('editCategoryIdInput').value = good.categoryOfGoodId || '';
    document.getElementById('editAnimalIdInput').value = good.animalId || '';
    document.getElementById('editGoodPriceInput').value = good.price || '';
    document.getElementById('editGoodImageURLInput').value = good.imageURL || '';
    document.getElementById('editGoodFormContainer').style.display = 'block';
    document.getElementById('editGoodFormSubmit').dataset.goodId = good.id; // Храним ID товара
}

// Редактирование товара
async function editGood() {
    const goodId = document.getElementById('editGoodFormSubmit').dataset.goodId;
    const title = document.getElementById('editGoodTitleInput').value.trim();
    const firmId = document.getElementById('editFirmIdInput').value.trim();
    const categoryId = document.getElementById('editCategoryIdInput').value.trim();
    const animalId = document.getElementById('editAnimalIdInput').value.trim();
    const price = parseFloat(document.getElementById('editGoodPriceInput').value.trim());
    const imageURL = document.getElementById('editGoodImageURLInput').value.trim();

    const payload = {
        title: title || undefined,
        firmId: firmId || undefined,
        categoryOfGoodId: categoryId || undefined,
        animalId: animalId || undefined,
        price: isNaN(price) ? undefined : price,
        imageURL: imageURL || undefined,
    };

    try {
        const response = await fetch(`${API_URL}/goods/${goodId}`, {
            method: 'PATCH',
            headers,
            body: JSON.stringify(payload),
        });

        if (response.ok) {
            console.log('Good updated successfully!');
            document.getElementById('editGoodFormContainer').style.display = 'none';
            loadGoods();
        } else {
            const errorData = await response.json();
            showError(errorData.detail || "Failed to edit good.");
        }
    } catch (error) {
        console.error(error);
        showError("An unexpected error occurred.");
    }
}

// События для формы редактирования
document.getElementById('editGoodFormSubmit').addEventListener('click', (e) => {
    e.preventDefault();
    editGood();
});

// Загрузка данных при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    loadGoods();
});
