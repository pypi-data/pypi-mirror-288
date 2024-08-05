from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class PollAnswer(TLObject):  # type: ignore
    __slots__: List[str] = ["text", "option"]

    ID = 0xff16e2ca
    QUALNAME = "types.PollAnswer"

    def __init__(self, *, text: "raw.base.TextWithEntities", option: bytes) -> None:
        self.text = text  # TextWithEntities
        self.option = option  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PollAnswer":
        # No flags
        
        text = TLObject.read(b)
        
        option = Bytes.read(b)
        
        return PollAnswer(text=text, option=option)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.text.write())
        
        b.write(Bytes(self.option))
        
        return b.getvalue()
