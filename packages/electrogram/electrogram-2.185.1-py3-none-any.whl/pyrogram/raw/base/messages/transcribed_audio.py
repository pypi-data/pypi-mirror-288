from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

TranscribedAudio = Union["raw.types.messages.TranscribedAudio"]


# noinspection PyRedeclaration
class TranscribedAudio:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.TranscribedAudio"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
