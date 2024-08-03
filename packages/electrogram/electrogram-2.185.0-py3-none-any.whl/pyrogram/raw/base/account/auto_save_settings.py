from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AutoSaveSettings = Union["raw.types.account.AutoSaveSettings"]


# noinspection PyRedeclaration
class AutoSaveSettings:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.AutoSaveSettings"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
