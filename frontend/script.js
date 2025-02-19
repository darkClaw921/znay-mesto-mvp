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
            if (typeFilter.value && place.type !== typeFilter.value) {
                return false;
            }
            // Здесь можно добавить фильтрацию по датам, если необходимо
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

    placeImage.src = place.image_url;
    placeName.textContent = place.name;
    placeType.textContent = place.type;
    placeDescription.textContent = place.description;
    placeContacts.textContent = place.contacts;

    placeInfo.classList.remove('hidden');
}

// Закрытие информации о месте
document.querySelector('.close-btn').addEventListener('click', () => {
    document.getElementById('place-info').classList.add('hidden');
});

// Функция для загрузки типов мест и заполнения select
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

// Инициализация карты при загрузке страницы
document.addEventListener('DOMContentLoaded', initMap);

// Вызываем функцию при загрузке страницы
document.addEventListener('DOMContentLoaded', loadPlaceTypes); 