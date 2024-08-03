from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PhoneCall = Union["raw.types.PhoneCall", "raw.types.PhoneCallAccepted", "raw.types.PhoneCallDiscarded", "raw.types.PhoneCallEmpty", "raw.types.PhoneCallRequested", "raw.types.PhoneCallWaiting"]


# noinspection PyRedeclaration
class PhoneCall:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PhoneCall"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
