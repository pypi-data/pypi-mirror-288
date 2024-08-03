from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DhConfig = Union["raw.types.messages.DhConfig", "raw.types.messages.DhConfigNotModified"]


# noinspection PyRedeclaration
class DhConfig:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.DhConfig"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
