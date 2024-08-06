from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class StarsStatus(TLObject):  # type: ignore
    __slots__: List[str] = ["balance", "history", "chats", "users", "next_offset"]

    ID = 0x8cf4ee60
    QUALNAME = "types.payments.StarsStatus"

    def __init__(self, *, balance: int, history: List["raw.base.StarsTransaction"], chats: List["raw.base.Chat"], users: List["raw.base.User"], next_offset: Optional[str] = None) -> None:
        self.balance = balance  # long
        self.history = history  # Vector<StarsTransaction>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.next_offset = next_offset  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarsStatus":
        
        flags = Int.read(b)
        
        balance = Long.read(b)
        
        history = TLObject.read(b)
        
        next_offset = String.read(b) if flags & (1 << 0) else None
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return StarsStatus(balance=balance, history=history, chats=chats, users=users, next_offset=next_offset)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.next_offset is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.balance))
        
        b.write(Vector(self.history))
        
        if self.next_offset is not None:
            b.write(String(self.next_offset))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
