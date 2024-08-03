from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PassportConfig = Union["raw.types.help.PassportConfig", "raw.types.help.PassportConfigNotModified"]


# noinspection PyRedeclaration
class PassportConfig:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.PassportConfig"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
