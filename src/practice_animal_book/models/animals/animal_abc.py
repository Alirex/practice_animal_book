import abc
import uuid
from typing import TYPE_CHECKING, TypeAlias
from uuid import uuid7

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from practice_animal_book.models.animals.animal_type import AnimalType
    from practice_animal_book.services.handlers.handler_output import T_RICH_FORMATTED_MESSAGE

T_ANIMAL_UID: TypeAlias = uuid.UUID


T_WEIGHT: TypeAlias = float
T_ANIMAL_NICKNAME: TypeAlias = str

T_SPEAK_MESSAGE: TypeAlias = str

T_FIELD_NAME: TypeAlias = str
T_FIELD_VALUE: TypeAlias = str
T_CLI_FIELDS: TypeAlias = dict[T_FIELD_NAME, T_FIELD_VALUE]


class AnimalOutput(BaseModel):
    uid: T_ANIMAL_UID
    nickname: T_ANIMAL_NICKNAME
    weight: T_WEIGHT

    extra_fields: T_CLI_FIELDS = Field(default_factory=dict)


class Animal(abc.ABC, BaseModel):
    uid: T_ANIMAL_UID = Field(default_factory=uuid7)
    nickname: T_ANIMAL_NICKNAME
    weight: T_WEIGHT

    @abc.abstractmethod
    def say(self) -> T_SPEAK_MESSAGE: ...

    def change_weight(self, weight: T_WEIGHT) -> None:
        self.weight = weight

    def get_extra_fields(self) -> T_CLI_FIELDS:
        cli_fields_data = self.model_dump(mode="json")
        # noinspection PyTypeChecker
        for field_name in Animal.model_fields:
            if field_name in cli_fields_data:
                del cli_fields_data[field_name]

        return {k: v for k, v in cli_fields_data.items() if v is not None}

    def get_cli(self) -> AnimalOutput:
        return AnimalOutput(
            uid=self.uid,
            nickname=self.nickname,
            weight=self.weight,
            extra_fields=self.get_extra_fields(),
        )

    def get_cli_output(self) -> T_RICH_FORMATTED_MESSAGE:
        return "\n".join((f"[green]{key}[/green]: {value}" for key, value in self.model_dump(mode="json")))  # type: ignore[misc,has-type]

    @abc.abstractmethod
    def get_animal_type(self) -> AnimalType: ...
