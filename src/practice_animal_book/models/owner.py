import uuid
from typing import NewType, TypedDict

from pydantic import BaseModel, Field


class OwnerInfo(TypedDict):
    name: str
    age: int
    address: str


OwnerUid = NewType("OwnerUid", uuid.UUID)


class Owner(BaseModel):
    uid: OwnerUid = Field(default_factory=lambda: OwnerUid(uuid.uuid7()))
    name: str
    age: int
    address: str

    def info(self) -> OwnerInfo:
        return OwnerInfo(
            name=self.name,
            age=self.age,
            address=self.address,
        )
