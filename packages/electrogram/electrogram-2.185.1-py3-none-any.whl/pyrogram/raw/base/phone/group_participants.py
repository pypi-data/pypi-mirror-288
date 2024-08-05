from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

GroupParticipants = Union["raw.types.phone.GroupParticipants"]


# noinspection PyRedeclaration
class GroupParticipants:  # type: ignore
    QUALNAME = "pyrogram.raw.base.phone.GroupParticipants"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
