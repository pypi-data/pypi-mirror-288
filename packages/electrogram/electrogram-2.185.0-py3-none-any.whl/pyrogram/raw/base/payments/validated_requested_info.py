from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ValidatedRequestedInfo = Union["raw.types.payments.ValidatedRequestedInfo"]


# noinspection PyRedeclaration
class ValidatedRequestedInfo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.payments.ValidatedRequestedInfo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
