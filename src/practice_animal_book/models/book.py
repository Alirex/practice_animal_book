from collections import UserDict

from practice_animal_book.models.animals.animal_abc import Animal, AnimalUid


class Book(UserDict[AnimalUid, Animal]):
    pass
