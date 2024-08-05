from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Themes = Union["raw.types.account.Themes", "raw.types.account.ThemesNotModified"]


# noinspection PyRedeclaration
class Themes:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.Themes"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
