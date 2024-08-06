from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class UpdateUserTyping(TLObject):  # type: ignore
    __slots__: List[str] = ["user_id", "action"]

    ID = 0xc01e857f
    QUALNAME = "types.UpdateUserTyping"

    def __init__(self, *, user_id: int, action: "raw.base.SendMessageAction") -> None:
        self.user_id = user_id  # long
        self.action = action  # SendMessageAction

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateUserTyping":
        # No flags
        
        user_id = Long.read(b)
        
        action = TLObject.read(b)
        
        return UpdateUserTyping(user_id=user_id, action=action)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.user_id))
        
        b.write(self.action.write())
        
        return b.getvalue()
