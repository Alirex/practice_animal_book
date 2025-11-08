import abc
import enum
import pathlib
import pickle
import uuid
from collections import UserDict
from typing import TYPE_CHECKING, Final, Self, TypeAlias, TypedDict
from uuid import uuid7

import rich.console
import rich.repr
import rich.table
from pydantic import BaseModel, ConfigDict, Field

from practice_animal_book.paths import FILES_PATH

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import TracebackType

T_WEIGHT: TypeAlias = float
T_ANIMAL_NICKNAME: TypeAlias = str


T_SPEAK_MESSAGE: TypeAlias = str

T_FIELD_NAME: TypeAlias = str
T_FIELD_VALUE: TypeAlias = str
T_CLI_FIELDS: TypeAlias = dict[T_FIELD_NAME, T_FIELD_VALUE]


T_ANIMAL_UID: TypeAlias = uuid.UUID


class AnimalOutput(BaseModel):
    uid: T_ANIMAL_UID
    nickname: T_ANIMAL_NICKNAME
    weight: T_WEIGHT

    extra_fields: T_CLI_FIELDS = Field(default_factory=dict)


class Animal(abc.ABC, BaseModel):
    uid: T_ANIMAL_UID = Field(default_factory=uuid7)
    nickname: T_ANIMAL_NICKNAME
    weight: T_WEIGHT

    @abc.abstractmethod
    def say(self) -> T_SPEAK_MESSAGE: ...

    def change_weight(self, weight: T_WEIGHT) -> None:
        self.weight = weight

    def get_extra_fields(self) -> T_CLI_FIELDS:
        cli_fields_data = self.model_dump(mode="json")
        for field_name in Animal.model_fields:
            if field_name not in cli_fields_data:
                del cli_fields_data[field_name]

        return cli_fields_data

    def get_cli(self) -> AnimalOutput:
        return AnimalOutput(
            uid=self.uid,
            nickname=self.nickname,
            weight=self.weight,
            extra_fields=self.get_extra_fields(),
        )

    def get_cli_output(self) -> T_OUTPUT_MESSAGE:
        return "\n".join((f"[green]{key}[/green]: {value}" for key, value in self.model_dump(mode="json")))  # type: ignore[misc,has-type]

    @abc.abstractmethod
    def get_animal_type(self) -> AnimalType: ...


class OwnerInfo(TypedDict):
    name: str
    age: int
    address: str


T_OWNER_UID: TypeAlias = uuid.UUID


class Owner(BaseModel):
    uid: T_ANIMAL_UID = Field(default_factory=uuid7)
    name: str
    age: int
    address: str

    def info(self) -> OwnerInfo:
        return OwnerInfo(
            name=self.name,
            age=self.age,
            address=self.address,
        )


class Dog(Animal):
    breed: str | None = None
    owner: Owner | None = None

    def say(self) -> T_SPEAK_MESSAGE:
        return "Woof"

    def who_is_owner(self) -> OwnerInfo | None:
        return None if self.owner is None else self.owner.info()

    def get_animal_type(self) -> AnimalType:
        return AnimalType.DOG


class Cat(Animal):
    def say(self) -> T_SPEAK_MESSAGE:
        return "Meow"

    def get_animal_type(self) -> AnimalType:
        return AnimalType.CAT


class Book(UserDict[T_ANIMAL_UID, Animal]):
    pass


class BookManager(BaseModel):
    path: pathlib.Path
    book: Book

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def load(cls, path: pathlib.Path) -> Self:
        try:
            with path.open("rb") as f:
                # noinspection PickleLoad
                book = pickle.load(f)  # noqa: S301
        except FileNotFoundError:
            book = Book()

        return cls(path=path, book=book)

    def __enter__(self) -> Book:
        return self.book

    def save(self, path: pathlib.Path) -> None:
        with path.open("wb") as f:
            # noinspection PyTypeChecker
            pickle.dump(self.book, f)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        self.save(self.path)
        return None


@enum.unique
class Action(enum.StrEnum):
    ANIMAL_ADD = "animal_add"
    ANIMAL_REMOVE = "animal_remove"
    ANIMALS_SHOW = "animals_show"

    DROP_BOOK = "drop_book"

    EXIT = "exit"


class HandlerOutput(BaseModel):
    message: T_OUTPUT_MESSAGE | None = None
    is_exit: bool = False


T_OUTPUT_MESSAGE: TypeAlias = str
T_ARGS: TypeAlias = list[str]


@enum.unique
class AnimalType(enum.StrEnum):
    DOG = "dog"
    CAT = "cat"


class AnimalTypeMeta(BaseModel):
    type_: AnimalType = Field(alias="type")
    title: str
    cls: type[Animal]


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


def animal_add(book: Book, args: T_ARGS) -> HandlerOutput:
    type_raw, nickname, weight = args

    type_ = AnimalType(type_raw.lower())

    animal_type_meta = ANIMAL_TYPE_MAPPING[type_]
    animal_class = animal_type_meta.cls
    animal = animal_class(nickname=nickname, weight=float(weight))

    book[animal.uid] = animal
    return HandlerOutput(message=f"Added {animal.nickname} with UID {animal.uid} to the book")


def animal_remove(book: Book, args: T_ARGS) -> HandlerOutput:
    uid_str = args[0]
    uid = uuid.UUID(uid_str)

    if uid not in book:
        return HandlerOutput(message=f"No animal with UID {uid_str} found in the book")

    removed_animal = book.pop(uid)
    return HandlerOutput(message=f"Removed {removed_animal.nickname} from the book")


# def animal_show(book: Book, args: T_ARGS) -> HandlerOutput:
#     uid_str = args[0]
#     uid = uuid.UUID(uid_str)
#
#     if uid not in book:
#         return HandlerOutput(message=f"No animal with UID {uid_str} found in the book")
#
#     animal = book[uid]
#     return HandlerOutput(message=animal.get_cli_output())


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
    print(len(book))
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


def drop_book(
    book: Book,
    args: T_ARGS,  # noqa: ARG001
) -> HandlerOutput:
    book.clear()
    return HandlerOutput(message="Book dropped")


def exit_handler(
    book: Book,  # noqa: ARG001
    args: T_ARGS,  # noqa: ARG001
) -> HandlerOutput:
    return HandlerOutput(message="Bye!", is_exit=True)


ACTIONS_MAPPING: dict[Action, Callable[[Book, T_ARGS], HandlerOutput]] = {
    Action.ANIMAL_ADD: animal_add,
    Action.ANIMAL_REMOVE: animal_remove,
    Action.ANIMALS_SHOW: animals_show,
    #
    Action.DROP_BOOK: drop_book,
    #
    Action.EXIT: exit_handler,
}


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
