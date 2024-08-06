from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputBotApp = Union["raw.types.InputBotAppID", "raw.types.InputBotAppShortName"]


# noinspection PyRedeclaration
class InputBotApp:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputBotApp"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
