from typing import TypeAlias

from pydantic import BaseModel, Field

T_RICH_FORMATTED_MESSAGE: TypeAlias = str
"""Rich formatted output message"""


class HandlerOutput(BaseModel):
    message: T_RICH_FORMATTED_MESSAGE | None = Field(
        default=None,
        description="Output message, that will be displayed to the user.",
    )
    is_exit: bool = Field(default=False, description="Exit the program")
