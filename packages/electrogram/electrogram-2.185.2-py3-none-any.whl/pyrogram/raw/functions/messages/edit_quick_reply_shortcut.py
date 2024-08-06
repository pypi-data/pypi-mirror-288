from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class EditQuickReplyShortcut(TLObject):  # type: ignore
    __slots__: List[str] = ["shortcut_id", "shortcut"]

    ID = 0x5c003cef
    QUALNAME = "functions.messages.EditQuickReplyShortcut"

    def __init__(self, *, shortcut_id: int, shortcut: str) -> None:
        self.shortcut_id = shortcut_id  # int
        self.shortcut = shortcut  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EditQuickReplyShortcut":
        # No flags
        
        shortcut_id = Int.read(b)
        
        shortcut = String.read(b)
        
        return EditQuickReplyShortcut(shortcut_id=shortcut_id, shortcut=shortcut)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.shortcut_id))
        
        b.write(String(self.shortcut))
        
        return b.getvalue()
