from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class UploadEncryptedFile(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "file"]

    ID = 0x5057c497
    QUALNAME = "functions.messages.UploadEncryptedFile"

    def __init__(self, *, peer: "raw.base.InputEncryptedChat", file: "raw.base.InputEncryptedFile") -> None:
        self.peer = peer  # InputEncryptedChat
        self.file = file  # InputEncryptedFile

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UploadEncryptedFile":
        # No flags
        
        peer = TLObject.read(b)
        
        file = TLObject.read(b)
        
        return UploadEncryptedFile(peer=peer, file=file)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.file.write())
        
        return b.getvalue()
