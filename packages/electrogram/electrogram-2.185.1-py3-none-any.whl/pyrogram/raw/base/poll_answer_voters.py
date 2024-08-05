from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PollAnswerVoters = Union["raw.types.PollAnswerVoters"]


# noinspection PyRedeclaration
class PollAnswerVoters:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PollAnswerVoters"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
