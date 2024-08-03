from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ReadParticipantDate = Union["raw.types.ReadParticipantDate"]


# noinspection PyRedeclaration
class ReadParticipantDate:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ReadParticipantDate"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
