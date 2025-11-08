import enum


@enum.unique
class Action(enum.StrEnum):
    ANIMAL_ADD = "animal_add"
    ANIMAL_REMOVE = "animal_remove"
    ANIMALS_SHOW = "animals_show"

    DROP_BOOK = "drop_book"

    EXIT = "exit"
