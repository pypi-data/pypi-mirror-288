from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class InputMessagesFilterChatPhotos(TLObject):  # type: ignore
    __slots__: List[str] = []

    ID = 0x3a20ecb8
    QUALNAME = "types.InputMessagesFilterChatPhotos"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputMessagesFilterChatPhotos":
        # No flags
        
        return InputMessagesFilterChatPhotos()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
