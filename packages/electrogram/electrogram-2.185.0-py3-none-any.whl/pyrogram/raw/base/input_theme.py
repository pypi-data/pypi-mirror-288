from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputTheme = Union["raw.types.InputTheme", "raw.types.InputThemeSlug"]


# noinspection PyRedeclaration
class InputTheme:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputTheme"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
