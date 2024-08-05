from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetCdnFileHashes(TLObject):  # type: ignore
    __slots__: List[str] = ["file_token", "offset"]

    ID = 0x91dc3f31
    QUALNAME = "functions.upload.GetCdnFileHashes"

    def __init__(self, *, file_token: bytes, offset: int) -> None:
        self.file_token = file_token  # bytes
        self.offset = offset  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetCdnFileHashes":
        # No flags
        
        file_token = Bytes.read(b)
        
        offset = Long.read(b)
        
        return GetCdnFileHashes(file_token=file_token, offset=offset)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.file_token))
        
        b.write(Long(self.offset))
        
        return b.getvalue()
