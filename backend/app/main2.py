from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from . import models, schemas, database
from typing import List
from .seed_data import seed_data
from .sync_bitrix import sync_places_from_bitrix
import os

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Монтируем статические файлы
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# Создание таблиц
models.Base.metadata.create_all(bind=database.engine)

# Зависимость для получения сессии БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    db = database.SessionLocal()
    try:
        # Проверяем, есть ли уже данные
        place_count = db.query(models.Place).count()
        if place_count == 0:
            seed_data(db)
    finally:
        db.close()

@app.get("/places/", response_model=List[schemas.Place])
def read_places(db: Session = Depends(get_db)):
    places = db.query(models.Place).all()
    return JSONResponse(
        content=[{
            "id": place.id,
            "name": place.name,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "type": place.type,
            "image_url": place.image_url,
            "contacts": place.contacts,
            "code": place.code,
            "bitrix_id": place.bitrix_id,
            "created_at": place.created_at,
            "modified_at": place.modified_at
        } for place in places],
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

@app.get("/places/{place_id}", response_model=schemas.Place)
def read_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="Место не найдено")
    return place

@app.get("/embed")
async def read_map_embed():
    return FileResponse(os.path.join(frontend_path, "map.html"))

@app.post("/sync-bitrix/")
async def sync_bitrix(db: Session = Depends(get_db)):
    try:
        await sync_places_from_bitrix(db)
        return {"message": "Синхронизация успешно завершена"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/place-types/")
def get_place_types(db: Session = Depends(get_db)):
    """Получает список уникальных типов мест из базы данных"""
    types = db.query(models.Place.type).distinct().all()
    # Преобразуем результат в список строк и удаляем None значения
    type_list = [t[0] for t in types if t[0] is not None]
    return JSONResponse(
        content=type_list,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)