from typing import TYPE_CHECKING

import rich.console
import rich.table

from practice_animal_book.models.animals.animal_type_mapping import ANIMAL_TYPE_MAPPING
from practice_animal_book.services.handlers.handler_output import HandlerOutput

if TYPE_CHECKING:
    from practice_animal_book.models.book import Book
    from practice_animal_book.services.parse_input import T_ARGS


# noinspection PyUnusedLocal
def animals_show(
    book: Book,
    args: T_ARGS,  # noqa: ARG001
) -> HandlerOutput:
    console = rich.console.Console()

    if not book:
        return HandlerOutput(message="No animals in the book")

    table = rich.table.Table(title="Animals")
    table.add_column("UID")
    table.add_column("Nickname")
    table.add_column("Weight")
    table.add_column("Type")
    table.add_column("Extra fields")

    for animal in book.values():
        animal_type = animal.get_animal_type()
        animal_type_meta = ANIMAL_TYPE_MAPPING[animal_type]

        table.add_row(
            str(animal.uid),
            animal.nickname,
            str(animal.weight),
            animal_type_meta.title,
            ",".join(f"[bold]{key}[/bold]: {value}" for key, value in animal.get_extra_fields().items()),
        )

    console.print(table)

    return HandlerOutput()
