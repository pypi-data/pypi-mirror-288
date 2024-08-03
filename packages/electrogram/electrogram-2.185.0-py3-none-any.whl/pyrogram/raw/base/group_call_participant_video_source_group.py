from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

GroupCallParticipantVideoSourceGroup = Union["raw.types.GroupCallParticipantVideoSourceGroup"]


# noinspection PyRedeclaration
class GroupCallParticipantVideoSourceGroup:  # type: ignore
    QUALNAME = "pyrogram.raw.base.GroupCallParticipantVideoSourceGroup"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
