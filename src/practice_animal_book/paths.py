import pathlib
from typing import Final

ROOT_PROJECT_PATH: Final[pathlib.Path] = pathlib.Path(__file__).parents[2]

FILES_PATH: Final[pathlib.Path] = ROOT_PROJECT_PATH / "files"
