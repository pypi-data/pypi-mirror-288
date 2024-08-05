from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DialogFilters = Union["raw.types.messages.DialogFilters"]


# noinspection PyRedeclaration
class DialogFilters:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.DialogFilters"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
