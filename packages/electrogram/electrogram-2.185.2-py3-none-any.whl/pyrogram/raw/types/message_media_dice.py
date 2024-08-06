from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class MessageMediaDice(TLObject):  # type: ignore
    __slots__: List[str] = ["value", "emoticon"]

    ID = 0x3f7ee58b
    QUALNAME = "types.MessageMediaDice"

    def __init__(self, *, value: int, emoticon: str) -> None:
        self.value = value  # int
        self.emoticon = emoticon  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageMediaDice":
        # No flags
        
        value = Int.read(b)
        
        emoticon = String.read(b)
        
        return MessageMediaDice(value=value, emoticon=emoticon)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.value))
        
        b.write(String(self.emoticon))
        
        return b.getvalue()
