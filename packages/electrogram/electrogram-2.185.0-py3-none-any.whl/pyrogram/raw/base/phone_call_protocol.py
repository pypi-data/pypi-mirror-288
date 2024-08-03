from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PhoneCallProtocol = Union["raw.types.PhoneCallProtocol"]


# noinspection PyRedeclaration
class PhoneCallProtocol:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PhoneCallProtocol"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
