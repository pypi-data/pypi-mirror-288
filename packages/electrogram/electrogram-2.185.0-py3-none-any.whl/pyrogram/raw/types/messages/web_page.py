from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class WebPage(TLObject):  # type: ignore
    __slots__: List[str] = ["webpage", "chats", "users"]

    ID = 0xfd5e12bd
    QUALNAME = "types.messages.WebPage"

    def __init__(self, *, webpage: "raw.base.WebPage", chats: List["raw.base.Chat"], users: List["raw.base.User"]) -> None:
        self.webpage = webpage  # WebPage
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "WebPage":
        # No flags
        
        webpage = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return WebPage(webpage=webpage, chats=chats, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.webpage.write())
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
