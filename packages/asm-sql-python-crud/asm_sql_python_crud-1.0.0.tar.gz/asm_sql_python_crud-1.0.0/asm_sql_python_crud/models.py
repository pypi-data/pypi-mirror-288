"""
...
"""

from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Session

#from base.managers import BaseManager

if TYPE_CHECKING:
    pass


class BaseModel(
    SQLModel,
    table=False
):
    """..."""

    #pk = "id"