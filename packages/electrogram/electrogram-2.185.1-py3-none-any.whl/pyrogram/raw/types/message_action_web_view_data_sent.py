from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class MessageActionWebViewDataSent(TLObject):  # type: ignore
    __slots__: List[str] = ["text"]

    ID = 0xb4c38cb5
    QUALNAME = "types.MessageActionWebViewDataSent"

    def __init__(self, *, text: str) -> None:
        self.text = text  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionWebViewDataSent":
        # No flags
        
        text = String.read(b)
        
        return MessageActionWebViewDataSent(text=text)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.text))
        
        return b.getvalue()
