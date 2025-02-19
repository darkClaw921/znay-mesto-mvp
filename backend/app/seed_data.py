from sqlalchemy.orm import Session
# import models
# import database
import models
import database

def seed_data(db: Session):
    # test_places = [
    #     {
    #         "name": "Парк Горького",
    #         "description": "Центральный парк культуры и отдыха им. Горького - главный парк столицы, с множеством развлечений, спортивных площадок и мест для отдыха.",
    #         "latitude": 55.731111,
    #         "longitude": 37.603056,
    #         "type": "Парк",
    #         "image_url": "https://example.com/gorky-park.jpg",
    #         "contacts": "ул. Крымский Вал, 9, Москва"
    #     },
    #     {
    #         "name": "ВДНХ",
    #         "description": "Выставка достижений народного хозяйства - уникальный архитектурно-парковый комплекс с выставками, музеями и развлечениями.",
    #         "latitude": 55.826479,
    #         "longitude": 37.637276,
    #         "type": "Парк",
    #         "image_url": "https://example.com/vdnh.jpg",
    #         "contacts": "пр-т Мира, 119, Москва"
    #     },
    #     {
    #         "name": "Коломенское",
    #         "description": "Музей-заповедник с древними церквями, царским дворцом и живописным парком на берегу Москвы-реки.",
    #         "latitude": 55.667539,
    #         "longitude": 37.668897,
    #         "type": "Музей",
    #         "image_url": "https://example.com/kolomenskoe.jpg",
    #         "contacts": "пр-т Андропова, 39, Москва"
    #     }
    # ]

    # for place_data in test_places:
    #     place = models.Place(**place_data)
    #     db.add(place)
    
    # db.commit()
    pass 