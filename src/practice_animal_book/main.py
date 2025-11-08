import rich.console
import rich.repr
import rich.table

from practice_animal_book.paths import FILES_PATH
from practice_animal_book.services.book_manager import BookManager
from practice_animal_book.services.handlers.actions_mapping import ACTIONS_MAPPING
from practice_animal_book.services.parse_input import parse_input


def main() -> None:
    with BookManager.load(path=FILES_PATH.joinpath("book.pkl")) as book:
        console = rich.console.Console()

        console.print("Welcome to the animal book!")
        while True:
            input_str = console.input("Enter an action: ")

            parsed_input = parse_input(input_str)
            console.print(parsed_input)

            action_func = ACTIONS_MAPPING[parsed_input.action]
            handler_output = action_func(book, parsed_input.args)
            if handler_output.message:
                console.print(handler_output.message)

            if handler_output.is_exit:
                return


if __name__ == "__main__":
    main()
