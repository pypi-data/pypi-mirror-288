from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DialogFilterSuggested = Union["raw.types.DialogFilterSuggested"]


# noinspection PyRedeclaration
class DialogFilterSuggested:  # type: ignore
    QUALNAME = "pyrogram.raw.base.DialogFilterSuggested"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
