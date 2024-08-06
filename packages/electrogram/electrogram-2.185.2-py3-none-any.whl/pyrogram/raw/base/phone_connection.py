from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PhoneConnection = Union["raw.types.PhoneConnection", "raw.types.PhoneConnectionWebrtc"]


# noinspection PyRedeclaration
class PhoneConnection:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PhoneConnection"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
