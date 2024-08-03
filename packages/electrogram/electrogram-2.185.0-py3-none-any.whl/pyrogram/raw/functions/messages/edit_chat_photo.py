from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class EditChatPhoto(TLObject):  # type: ignore
    __slots__: List[str] = ["chat_id", "photo"]

    ID = 0x35ddd674
    QUALNAME = "functions.messages.EditChatPhoto"

    def __init__(self, *, chat_id: int, photo: "raw.base.InputChatPhoto") -> None:
        self.chat_id = chat_id  # long
        self.photo = photo  # InputChatPhoto

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EditChatPhoto":
        # No flags
        
        chat_id = Long.read(b)
        
        photo = TLObject.read(b)
        
        return EditChatPhoto(chat_id=chat_id, photo=photo)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.chat_id))
        
        b.write(self.photo.write())
        
        return b.getvalue()
