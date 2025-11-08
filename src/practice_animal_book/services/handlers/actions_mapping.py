from collections.abc import Callable
from typing import TypeAlias

from practice_animal_book.models.book import Book
from practice_animal_book.services.handlers.action import Action
from practice_animal_book.services.handlers.elements.animal_add import animal_add
from practice_animal_book.services.handlers.elements.animal_remove import animal_remove
from practice_animal_book.services.handlers.elements.animals_show import animals_show
from practice_animal_book.services.handlers.elements.drop_book import drop_book
from practice_animal_book.services.handlers.elements.exit_handler import exit_handler
from practice_animal_book.services.handlers.handler_output import HandlerOutput
from practice_animal_book.services.parse_input import T_ARGS

T_ACTION_HANDLER: TypeAlias = Callable[[Book, T_ARGS], HandlerOutput]
"""Action handler"""

ACTIONS_MAPPING: dict[Action, T_ACTION_HANDLER] = {
    Action.ANIMAL_ADD: animal_add,
    Action.ANIMAL_REMOVE: animal_remove,
    Action.ANIMALS_SHOW: animals_show,
    #
    Action.DROP_BOOK: drop_book,
    #
    Action.EXIT: exit_handler,
}
