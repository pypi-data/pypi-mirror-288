from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

GroupCallParticipant = Union["raw.types.GroupCallParticipant"]


# noinspection PyRedeclaration
class GroupCallParticipant:  # type: ignore
    QUALNAME = "pyrogram.raw.base.GroupCallParticipant"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
