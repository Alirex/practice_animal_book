import pathlib
import pickle
from typing import TYPE_CHECKING, Self

from pydantic import BaseModel, ConfigDict

from practice_animal_book.models.book import Book

if TYPE_CHECKING:
    from types import TracebackType


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
