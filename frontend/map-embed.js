let map;
let markers = [];
let allPlaces = [];

async function initMap() {
    // Инициализация карты
    map = L.map('map').setView([55.7558, 37.6173], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    await loadPlaces();
    setupFilters();
}

async function loadPlaces() {
    try {
        const response = await fetch('/places/', {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });
        allPlaces = await response.json();
        displayPlaces(allPlaces);
    } catch (error) {
        console.error('Ошибка при загрузке мест:', error);
    }
}

function displayPlaces(places) {
    // Очищаем существующие маркеры
    markers.forEach(marker => marker.remove());
    markers = [];
    
    places.forEach(place => {
        const marker = L.marker([place.latitude, place.longitude])
            .addTo(map)
            .bindPopup(`
                <h3>${place.name}</h3>
                <p>${place.type}</p>
                <button onclick="showPlaceInfo(${JSON.stringify(place).replace(/"/g, '&quot;')})">
                    Подробнее
                </button>
            `);
        markers.push(marker);
    });
}

function setupFilters() {
    const filtersButton = document.getElementById('filters-button');
    const filtersPanel = document.getElementById('filters-panel');
    const applyFilters = document.getElementById('apply-filters');
    const clearFilters = document.querySelector('.clear-filters');
    const typeFilter = document.getElementById('type-filter');
    const startDate = document.getElementById('start-date');
    const endDate = document.getElementById('end-date');

    // Показать/скрыть панель фильтров
    filtersButton.addEventListener('click', () => {
        filtersPanel.classList.toggle('hidden');
    });

    // Применить фильтры
    applyFilters.addEventListener('click', () => {
        const filteredPlaces = allPlaces.filter(place => {
            const searchText = document.getElementById('search-input').value.toLowerCase();
            if (typeFilter.value && place.type !== typeFilter.value) {
                return false;
            }
            // Поиск по описанию и названию
            if (searchText) {
                const searchIn = [
                    place.name,
                    place.description,
                    place.type,
                    place.contacts
                ].map(text => text.toLowerCase());
                
                // Разбиваем поисковый запрос на слова
                const searchWords = searchText.split(' ');
                
                // Проверяем, что хотя бы одно слово найдено в любом из полей
                const found = searchWords.some(word => 
                    searchIn.some(field => field.includes(word))
                );
                
                if (!found) return false;
            }
            return true;
        });
        
        displayPlaces(filteredPlaces);
        filtersPanel.classList.add('hidden');
    });

    // Очистить фильтры
    clearFilters.addEventListener('click', () => {
        typeFilter.value = '';
        startDate.value = '';
        endDate.value = '';
        document.getElementById('search-input').value = '';
        displayPlaces(allPlaces);
    });
}

function showPlaceInfo(place) {
    const placeInfo = document.getElementById('place-info');
    const placeImage = document.getElementById('place-image');
    const placeName = document.getElementById('place-name');
    const placeType = document.getElementById('place-type');
    const placeDescription = document.getElementById('place-description');
    const placeContacts = document.getElementById('place-contacts');
    const placeLink = document.getElementById('place-link');

    placeImage.src = place.image_url;
    placeName.textContent = place.name;
    placeType.textContent = place.type;
    placeDescription.textContent = place.description;
    placeContacts.textContent = place.contacts;
    placeLink.href = `https://znayu-mesto.bitrix24shop.ru/katalog/item/${place.code}/`;

    placeInfo.classList.remove('hidden');
}

// Закрытие информации о месте
document.querySelector('.close-btn').addEventListener('click', () => {
    document.getElementById('place-info').classList.add('hidden');
});

async function loadPlaceTypes() {
    try {
        const response = await fetch('/place-types/');
        const types = await response.json();
        
        const typeFilter = document.getElementById('type-filter');
        // Сохраняем текущее выбранное значение
        const currentValue = typeFilter.value;
        
        // Очищаем текущие опции, оставляя только первую (Любой)
        while (typeFilter.options.length > 1) {
            typeFilter.remove(1);
        }
        
        // Добавляем новые опции
        types.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            typeFilter.appendChild(option);
        });
        
        // Восстанавливаем выбранное значение
        if (types.includes(currentValue)) {
            typeFilter.value = currentValue;
        }
    } catch (error) {
        console.error('Ошибка при загрузке типов мест:', error);
    }
}

// Изменяем инициализацию при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    await initMap();
    await loadPlaceTypes();
}); 