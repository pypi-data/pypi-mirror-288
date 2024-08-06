from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InviteText = Union["raw.types.help.InviteText"]


# noinspection PyRedeclaration
class InviteText:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.InviteText"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
