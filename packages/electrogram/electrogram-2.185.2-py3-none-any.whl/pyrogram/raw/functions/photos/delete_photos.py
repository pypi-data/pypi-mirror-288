from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class DeletePhotos(TLObject):  # type: ignore
    __slots__: List[str] = ["id"]

    ID = 0x87cf7f2f
    QUALNAME = "functions.photos.DeletePhotos"

    def __init__(self, *, id: List["raw.base.InputPhoto"]) -> None:
        self.id = id  # Vector<InputPhoto>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DeletePhotos":
        # No flags
        
        id = TLObject.read(b)
        
        return DeletePhotos(id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.id))
        
        return b.getvalue()
