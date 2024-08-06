from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PhoneCall = Union["raw.types.phone.PhoneCall"]


# noinspection PyRedeclaration
class PhoneCall:  # type: ignore
    QUALNAME = "pyrogram.raw.base.phone.PhoneCall"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
