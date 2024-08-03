from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class StoryViewPublicForward(TLObject):  # type: ignore
    __slots__: List[str] = ["message", "blocked", "blocked_my_stories_from"]

    ID = 0x9083670b
    QUALNAME = "types.StoryViewPublicForward"

    def __init__(self, *, message: "raw.base.Message", blocked: Optional[bool] = None, blocked_my_stories_from: Optional[bool] = None) -> None:
        self.message = message  # Message
        self.blocked = blocked  # flags.0?true
        self.blocked_my_stories_from = blocked_my_stories_from  # flags.1?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StoryViewPublicForward":
        
        flags = Int.read(b)
        
        blocked = True if flags & (1 << 0) else False
        blocked_my_stories_from = True if flags & (1 << 1) else False
        message = TLObject.read(b)
        
        return StoryViewPublicForward(message=message, blocked=blocked, blocked_my_stories_from=blocked_my_stories_from)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.blocked else 0
        flags |= (1 << 1) if self.blocked_my_stories_from else 0
        b.write(Int(flags))
        
        b.write(self.message.write())
        
        return b.getvalue()
