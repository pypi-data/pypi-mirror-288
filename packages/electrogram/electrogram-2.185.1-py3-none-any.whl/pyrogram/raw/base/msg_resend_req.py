from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MsgResendReq = Union["raw.types.MsgResendAnsReq", "raw.types.MsgResendReq"]


# noinspection PyRedeclaration
class MsgResendReq:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MsgResendReq"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
