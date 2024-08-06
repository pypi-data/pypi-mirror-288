from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SmsJob = Union["raw.types.SmsJob"]


# noinspection PyRedeclaration
class SmsJob:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SmsJob"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
