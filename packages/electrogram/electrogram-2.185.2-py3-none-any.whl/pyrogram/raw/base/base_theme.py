from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BaseTheme = Union["raw.types.BaseThemeArctic", "raw.types.BaseThemeClassic", "raw.types.BaseThemeDay", "raw.types.BaseThemeNight", "raw.types.BaseThemeTinted"]


# noinspection PyRedeclaration
class BaseTheme:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BaseTheme"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
