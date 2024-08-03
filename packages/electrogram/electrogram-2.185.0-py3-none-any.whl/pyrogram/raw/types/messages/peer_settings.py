from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class PeerSettings(TLObject):  # type: ignore
    __slots__: List[str] = ["settings", "chats", "users"]

    ID = 0x6880b94d
    QUALNAME = "types.messages.PeerSettings"

    def __init__(self, *, settings: "raw.base.PeerSettings", chats: List["raw.base.Chat"], users: List["raw.base.User"]) -> None:
        self.settings = settings  # PeerSettings
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PeerSettings":
        # No flags
        
        settings = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return PeerSettings(settings=settings, chats=chats, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.settings.write())
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
