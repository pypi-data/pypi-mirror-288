from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AppConfig = Union["raw.types.help.AppConfig", "raw.types.help.AppConfigNotModified"]


# noinspection PyRedeclaration
class AppConfig:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.AppConfig"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
