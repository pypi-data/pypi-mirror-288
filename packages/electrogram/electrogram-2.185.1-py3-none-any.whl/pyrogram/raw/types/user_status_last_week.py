from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class UserStatusLastWeek(TLObject):  # type: ignore
    __slots__: List[str] = ["by_me"]

    ID = 0x541a1d1a
    QUALNAME = "types.UserStatusLastWeek"

    def __init__(self, *, by_me: Optional[bool] = None) -> None:
        self.by_me = by_me  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UserStatusLastWeek":
        
        flags = Int.read(b)
        
        by_me = True if flags & (1 << 0) else False
        return UserStatusLastWeek(by_me=by_me)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.by_me else 0
        b.write(Int(flags))
        
        return b.getvalue()
