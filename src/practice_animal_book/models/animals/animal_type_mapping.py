from typing import Final

from practice_animal_book.models.animals.animal_type import AnimalType
from practice_animal_book.models.animals.animal_type_meta import AnimalTypeMeta
from practice_animal_book.models.animals.cat import Cat
from practice_animal_book.models.animals.dog import Dog

ANIMAL_TYPE_MAPPING: Final[dict[AnimalType, AnimalTypeMeta]] = {
    item.type_: item
    for item in [
        AnimalTypeMeta(
            type=AnimalType.CAT,
            title="Cat",
            cls=Cat,
        ),
        AnimalTypeMeta(
            type=AnimalType.DOG,
            title="Dog",
            cls=Dog,
        ),
    ]
}
