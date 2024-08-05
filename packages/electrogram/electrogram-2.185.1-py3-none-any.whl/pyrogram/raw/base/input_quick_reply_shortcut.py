from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputQuickReplyShortcut = Union["raw.types.InputQuickReplyShortcut", "raw.types.InputQuickReplyShortcutId"]


# noinspection PyRedeclaration
class InputQuickReplyShortcut:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputQuickReplyShortcut"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
