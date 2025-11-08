from pydantic import BaseModel, Field

from practice_animal_book.models.animals.animal_abc import Animal
from practice_animal_book.models.animals.animal_type import AnimalType


class AnimalTypeMeta(BaseModel):
    type_: AnimalType = Field(alias="type")
    title: str
    cls: type[Animal]
