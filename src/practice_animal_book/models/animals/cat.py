from practice_animal_book.models.animals.animal_abc import T_SPEAK_MESSAGE, Animal
from practice_animal_book.models.animals.animal_type import AnimalType


class Cat(Animal):
    def say(self) -> T_SPEAK_MESSAGE:
        return "Meow"

    def get_animal_type(self) -> AnimalType:
        return AnimalType.CAT
