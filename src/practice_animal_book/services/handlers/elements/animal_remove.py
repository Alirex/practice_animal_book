import uuid
from typing import TYPE_CHECKING

from practice_animal_book.models.animals.animal_abc import AnimalUid
from practice_animal_book.services.handlers.handler_output import HandlerOutput

if TYPE_CHECKING:
    from practice_animal_book.models.book import Book
    from practice_animal_book.services.parse_input import T_ARGS


def animal_remove(book: Book, args: T_ARGS) -> HandlerOutput:
    uid_str = args[0]
    uid = AnimalUid(uuid.UUID(uid_str))

    if uid not in book:
        return HandlerOutput(message=f"No animal with UID {uid_str} found in the book")

    removed_animal = book.pop(uid)
    return HandlerOutput(message=f"Removed {removed_animal.nickname} from the book")
