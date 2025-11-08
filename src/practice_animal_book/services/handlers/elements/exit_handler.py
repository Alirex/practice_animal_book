from typing import TYPE_CHECKING

from practice_animal_book.services.handlers.handler_output import HandlerOutput

if TYPE_CHECKING:
    from practice_animal_book.models.book import Book
    from practice_animal_book.services.parse_input import T_ARGS


# noinspection PyUnusedLocal
def exit_handler(
    book: Book,  # noqa: ARG001
    args: T_ARGS,  # noqa: ARG001
) -> HandlerOutput:
    return HandlerOutput(message="\nBye!", is_exit=True)
