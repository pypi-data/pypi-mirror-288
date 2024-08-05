from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ResetPasswordResult = Union["raw.types.account.ResetPasswordFailedWait", "raw.types.account.ResetPasswordOk", "raw.types.account.ResetPasswordRequestedWait"]


# noinspection PyRedeclaration
class ResetPasswordResult:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.ResetPasswordResult"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
