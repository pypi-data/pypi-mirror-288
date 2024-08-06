from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class MessageActionChatCreate(TLObject):  # type: ignore
    __slots__: List[str] = ["title", "users"]

    ID = 0xbd47cbad
    QUALNAME = "types.MessageActionChatCreate"

    def __init__(self, *, title: str, users: List[int]) -> None:
        self.title = title  # string
        self.users = users  # Vector<long>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionChatCreate":
        # No flags
        
        title = String.read(b)
        
        users = TLObject.read(b, Long)
        
        return MessageActionChatCreate(title=title, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.title))
        
        b.write(Vector(self.users, Long))
        
        return b.getvalue()
