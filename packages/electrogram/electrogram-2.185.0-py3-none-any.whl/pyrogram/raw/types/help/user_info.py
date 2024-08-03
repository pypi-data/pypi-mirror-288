from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class UserInfo(TLObject):  # type: ignore
    __slots__: List[str] = ["message", "entities", "author", "date"]

    ID = 0x1eb3758
    QUALNAME = "types.help.UserInfo"

    def __init__(self, *, message: str, entities: List["raw.base.MessageEntity"], author: str, date: int) -> None:
        self.message = message  # string
        self.entities = entities  # Vector<MessageEntity>
        self.author = author  # string
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UserInfo":
        # No flags
        
        message = String.read(b)
        
        entities = TLObject.read(b)
        
        author = String.read(b)
        
        date = Int.read(b)
        
        return UserInfo(message=message, entities=entities, author=author, date=date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.message))
        
        b.write(Vector(self.entities))
        
        b.write(String(self.author))
        
        b.write(Int(self.date))
        
        return b.getvalue()
