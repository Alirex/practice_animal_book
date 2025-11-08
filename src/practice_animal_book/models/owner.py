import uuid
from typing import TypeAlias, TypedDict

from pydantic import BaseModel, Field

from practice_animal_book.models.animals.animal_abc import T_ANIMAL_UID


class OwnerInfo(TypedDict):
    name: str
    age: int
    address: str


T_OWNER_UID: TypeAlias = uuid.UUID


class Owner(BaseModel):
    uid: T_ANIMAL_UID = Field(default_factory=uuid.uuid7)
    name: str
    age: int
    address: str

    def info(self) -> OwnerInfo:
        return OwnerInfo(
            name=self.name,
            age=self.age,
            address=self.address,
        )
