from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

State = Union["raw.types.updates.State"]


# noinspection PyRedeclaration
class State:  # type: ignore
    QUALNAME = "pyrogram.raw.base.updates.State"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
