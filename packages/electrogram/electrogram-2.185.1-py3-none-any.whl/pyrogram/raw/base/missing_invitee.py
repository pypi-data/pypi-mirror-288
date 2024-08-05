from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MissingInvitee = Union["raw.types.MissingInvitee"]


# noinspection PyRedeclaration
class MissingInvitee:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MissingInvitee"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
