from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InlineBotSwitchPM = Union["raw.types.InlineBotSwitchPM"]


# noinspection PyRedeclaration
class InlineBotSwitchPM:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InlineBotSwitchPM"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
