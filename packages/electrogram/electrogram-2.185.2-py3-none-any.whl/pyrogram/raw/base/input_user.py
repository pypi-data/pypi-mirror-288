from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputUser = Union["raw.types.InputUser", "raw.types.InputUserEmpty", "raw.types.InputUserFromMessage", "raw.types.InputUserSelf"]


# noinspection PyRedeclaration
class InputUser:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputUser"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
