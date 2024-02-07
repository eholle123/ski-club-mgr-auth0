from pydantic import BaseModel

class SkiPassCreate(BaseModel):
    serial_number: str

class SkiPassPublic(BaseModel):
    serial_number: str
    is_invalidated: bool