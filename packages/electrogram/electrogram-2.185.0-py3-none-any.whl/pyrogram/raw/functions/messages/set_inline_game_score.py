from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SetInlineGameScore(TLObject):  # type: ignore
    __slots__: List[str] = ["id", "user_id", "score", "edit_message", "force"]

    ID = 0x15ad9f64
    QUALNAME = "functions.messages.SetInlineGameScore"

    def __init__(self, *, id: "raw.base.InputBotInlineMessageID", user_id: "raw.base.InputUser", score: int, edit_message: Optional[bool] = None, force: Optional[bool] = None) -> None:
        self.id = id  # InputBotInlineMessageID
        self.user_id = user_id  # InputUser
        self.score = score  # int
        self.edit_message = edit_message  # flags.0?true
        self.force = force  # flags.1?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetInlineGameScore":
        
        flags = Int.read(b)
        
        edit_message = True if flags & (1 << 0) else False
        force = True if flags & (1 << 1) else False
        id = TLObject.read(b)
        
        user_id = TLObject.read(b)
        
        score = Int.read(b)
        
        return SetInlineGameScore(id=id, user_id=user_id, score=score, edit_message=edit_message, force=force)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.edit_message else 0
        flags |= (1 << 1) if self.force else 0
        b.write(Int(flags))
        
        b.write(self.id.write())
        
        b.write(self.user_id.write())
        
        b.write(Int(self.score))
        
        return b.getvalue()
