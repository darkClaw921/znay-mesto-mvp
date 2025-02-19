from sqlalchemy.orm import Session
from . import models, database
from .work_bitrix import get_all_products, Catalog
import asyncio
from pprint import pprint
catalog = Catalog()
async def sync_places_from_bitrix(db: Session):
    # Получаем все товары из Битрикса
    section_mapping1 = {
        catalog.ohota: 'Охота',
        catalog.rybalka: 'Рыбалка',
        catalog.kulturniy_turizm: 'Культурный туризм и пеший туризм',
        catalog.priklyuchenie: 'Приключенческий туризм и альпинизм',
        catalog.eko_turizm: 'Экотуризм и кемпинг',
        catalog.plazh_turizm: 'Пляжный туризм и водные виды спорта',
        catalog.gastronomic_turizm: 'Гастрономический туризм',
        catalog.medical_turizm: 'Медицинский туризм',
        catalog.sport_turizm: 'Спортивный туризм и спортивные игры',
        catalog.religioznyy_turizm: 'Религиозный туризм',
        catalog.business_turizm: 'Деловой туризм',
        catalog.agroturizm: 'Агротуризм и велосипедный спорт',
        catalog.zimniye_vidy_sporta: 'Зимние виды спорта',
        catalog.bеg_i_marafony: 'Бег и марафоны',
        catalog.parakliniizm_i_deltaplanirizm: 'Парапланеризм и дельтапланеризм',
        catalog.yogi_i_fitnes: 'Йога и фитнес на свежем воздухе',
        catalog.gribnictvo: 'Грибничество',
        catalog.orekhodstvo: 'Ореховодство',
        catalog.sbir_dikorastuyushchikh_plodov: 'Сбор дикорастущих плодов',
        catalog.travnictvo: 'Травничество',
        catalog.yagodnictvo: 'Ягодничество',
    }
    
    products = await get_all_products()
    
    for product in products:
        # Получаем координаты из свойства PROPERTY_107
        coordinates = None
        pprint(product)
        if 'PROPERTY_107' in product and product['PROPERTY_107']:
            coordinates = product['PROPERTY_107']['value'].split(',')
            
        if not coordinates or len(coordinates) != 2:
            print(f"Пропускаем товар {product['NAME']}: нет координат")
            continue
            
        try:
            latitude = float(coordinates[0].strip())
            longitude = float(coordinates[1].strip())
        except ValueError:
            print(f"Пропускаем товар {product['NAME']}: неверный формат координат")
            continue

        # Проверяем существование места по bitrix_id
        existing_place = db.query(models.Place).filter(
            models.Place.bitrix_id == product['ID']
        ).first()

        place_data = {
            "name": product['NAME'],
            "description": product['DESCRIPTION'] or "",
            "latitude": latitude,
            "longitude": longitude,
            "type": section_mapping1[int(product['SECTION_ID'])],
            "image_url": product.get('PREVIEW_PICTURE', "https://example.com/placeholder.jpg"),
            "contacts": "",  # Можно добавить контакты из других полей Битрикса
            "code": product['CODE'],
            "bitrix_id": product['ID'],
            "created_at": product['DATE_CREATE'],
            "modified_at": product['TIMESTAMP_X']
        }

        if existing_place:
            # Обновляем существующее место
            for key, value in place_data.items():
                setattr(existing_place, key, value)
        else:
            # Создаем новое место
            place = models.Place(**place_data)
            db.add(place)

    try:
        db.commit()
        print("Синхронизация с Битриксом завершена успешно")
    except Exception as e:
        print(f"Ошибка при синхронизации с Битриксом: {e}")
        db.rollback() 