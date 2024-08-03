from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class Stories(TLObject):  # type: ignore
    __slots__: List[str] = ["count", "stories", "chats", "users", "pinned_to_top"]

    ID = 0x63c3dd0a
    QUALNAME = "types.stories.Stories"

    def __init__(self, *, count: int, stories: List["raw.base.StoryItem"], chats: List["raw.base.Chat"], users: List["raw.base.User"], pinned_to_top: Optional[List[int]] = None) -> None:
        self.count = count  # int
        self.stories = stories  # Vector<StoryItem>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.pinned_to_top = pinned_to_top  # flags.0?Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Stories":
        
        flags = Int.read(b)
        
        count = Int.read(b)
        
        stories = TLObject.read(b)
        
        pinned_to_top = TLObject.read(b, Int) if flags & (1 << 0) else []
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return Stories(count=count, stories=stories, chats=chats, users=users, pinned_to_top=pinned_to_top)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.pinned_to_top else 0
        b.write(Int(flags))
        
        b.write(Int(self.count))
        
        b.write(Vector(self.stories))
        
        if self.pinned_to_top is not None:
            b.write(Vector(self.pinned_to_top, Int))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
