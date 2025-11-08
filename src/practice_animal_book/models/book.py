from collections import UserDict

from practice_animal_book.models.animals.animal_abc import T_ANIMAL_UID, Animal


class Book(UserDict[T_ANIMAL_UID, Animal]):
    pass
