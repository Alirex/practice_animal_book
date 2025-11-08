from typing import TYPE_CHECKING, TypeAlias

from pydantic import BaseModel

from practice_animal_book.services.handlers.action import Action

if TYPE_CHECKING:
    import rich.repr


T_ARGS: TypeAlias = list[str]


class ParsedInput(BaseModel):
    action: Action
    args: T_ARGS

    def __rich_repr__(self) -> rich.repr.Result:
        # https://rich.readthedocs.io/en/latest/pretty.html#typing
        yield str(self.action)
        yield self.args


def parse_input(input_str: str) -> ParsedInput:
    action_raw, *args = input_str.split()
    action = Action(action_raw)
    return ParsedInput(action=action, args=args)
