from typing import Optional
from sqlmodel import Field, SQLModel


class SkiPass(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    serial_number: str
    is_invalidated: bool = False
