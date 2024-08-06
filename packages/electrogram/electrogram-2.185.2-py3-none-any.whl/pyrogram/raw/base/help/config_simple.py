from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ConfigSimple = Union["raw.types.help.ConfigSimple"]


# noinspection PyRedeclaration
class ConfigSimple:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.ConfigSimple"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
