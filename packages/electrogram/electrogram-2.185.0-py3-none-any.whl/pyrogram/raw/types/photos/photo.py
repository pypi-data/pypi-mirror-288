from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class Photo(TLObject):  # type: ignore
    __slots__: List[str] = ["photo", "users"]

    ID = 0x20212ca8
    QUALNAME = "types.photos.Photo"

    def __init__(self, *, photo: "raw.base.Photo", users: List["raw.base.User"]) -> None:
        self.photo = photo  # Photo
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Photo":
        # No flags
        
        photo = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return Photo(photo=photo, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.photo.write())
        
        b.write(Vector(self.users))
        
        return b.getvalue()
