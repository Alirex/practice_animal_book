from typing import TYPE_CHECKING

from practice_animal_book.models.animals.animal_abc import T_SPEAK_MESSAGE, Animal
from practice_animal_book.models.animals.animal_type import AnimalType
from practice_animal_book.models.owner import Owner  # noqa: TC001

if TYPE_CHECKING:
    from practice_animal_book.models.owner import OwnerInfo


class Dog(Animal):
    breed: str | None = None
    owner: Owner | None = None

    def say(self) -> T_SPEAK_MESSAGE:
        return "Woof"

    def who_is_owner(self) -> OwnerInfo | None:
        return None if self.owner is None else self.owner.info()

    def get_animal_type(self) -> AnimalType:
        return AnimalType.DOG
