from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class MessageActionInviteToGroupCall(TLObject):  # type: ignore
    __slots__: List[str] = ["call", "users"]

    ID = 0x502f92f7
    QUALNAME = "types.MessageActionInviteToGroupCall"

    def __init__(self, *, call: "raw.base.InputGroupCall", users: List[int]) -> None:
        self.call = call  # InputGroupCall
        self.users = users  # Vector<long>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionInviteToGroupCall":
        # No flags
        
        call = TLObject.read(b)
        
        users = TLObject.read(b, Long)
        
        return MessageActionInviteToGroupCall(call=call, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.call.write())
        
        b.write(Vector(self.users, Long))
        
        return b.getvalue()
