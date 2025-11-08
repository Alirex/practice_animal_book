from typing import TYPE_CHECKING

from practice_animal_book.models.animals.animal_type import AnimalType
from practice_animal_book.models.animals.animal_type_mapping import ANIMAL_TYPE_MAPPING
from practice_animal_book.services.handlers.handler_output import HandlerOutput

if TYPE_CHECKING:
    from practice_animal_book.models.book import Book
    from practice_animal_book.services.parse_input import T_ARGS


def animal_add(book: Book, args: T_ARGS) -> HandlerOutput:
    type_raw, nickname, weight = args

    type_ = AnimalType(type_raw.lower())

    animal_type_meta = ANIMAL_TYPE_MAPPING[type_]
    animal_class = animal_type_meta.cls
    animal = animal_class(nickname=nickname, weight=float(weight))

    book[animal.uid] = animal
    return HandlerOutput(message=f"Added {animal.nickname} with UID {animal.uid} to the book")
