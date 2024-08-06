from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputChannel = Union["raw.types.InputChannel", "raw.types.InputChannelEmpty", "raw.types.InputChannelFromMessage"]


# noinspection PyRedeclaration
class InputChannel:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputChannel"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
