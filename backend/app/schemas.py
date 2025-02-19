from pydantic import BaseModel, ConfigDict

class PlaceBase(BaseModel):
    name: str
    description: str
    latitude: float
    longitude: float
    type: str
    image_url: str
    contacts: str
    code: str
    bitrix_id: str
    created_at: str
    modified_at: str

    model_config = ConfigDict(from_attributes=True)

class PlaceCreate(PlaceBase):
    pass

class Place(PlaceBase):
    id: int 