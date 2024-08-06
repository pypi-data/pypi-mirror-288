from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

TextWithEntities = Union["raw.types.TextWithEntities"]


# noinspection PyRedeclaration
class TextWithEntities:  # type: ignore
    QUALNAME = "pyrogram.raw.base.TextWithEntities"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
