from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class InputPaymentCredentialsSaved(TLObject):  # type: ignore
    __slots__: List[str] = ["id", "tmp_password"]

    ID = 0xc10eb2cf
    QUALNAME = "types.InputPaymentCredentialsSaved"

    def __init__(self, *, id: str, tmp_password: bytes) -> None:
        self.id = id  # string
        self.tmp_password = tmp_password  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPaymentCredentialsSaved":
        # No flags
        
        id = String.read(b)
        
        tmp_password = Bytes.read(b)
        
        return InputPaymentCredentialsSaved(id=id, tmp_password=tmp_password)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.id))
        
        b.write(Bytes(self.tmp_password))
        
        return b.getvalue()
