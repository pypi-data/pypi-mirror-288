from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class UpdateUserName(TLObject):  # type: ignore
    __slots__: List[str] = ["user_id", "first_name", "last_name", "usernames"]

    ID = 0xa7848924
    QUALNAME = "types.UpdateUserName"

    def __init__(self, *, user_id: int, first_name: str, last_name: str, usernames: List["raw.base.Username"]) -> None:
        self.user_id = user_id  # long
        self.first_name = first_name  # string
        self.last_name = last_name  # string
        self.usernames = usernames  # Vector<Username>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateUserName":
        # No flags
        
        user_id = Long.read(b)
        
        first_name = String.read(b)
        
        last_name = String.read(b)
        
        usernames = TLObject.read(b)
        
        return UpdateUserName(user_id=user_id, first_name=first_name, last_name=last_name, usernames=usernames)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.user_id))
        
        b.write(String(self.first_name))
        
        b.write(String(self.last_name))
        
        b.write(Vector(self.usernames))
        
        return b.getvalue()
