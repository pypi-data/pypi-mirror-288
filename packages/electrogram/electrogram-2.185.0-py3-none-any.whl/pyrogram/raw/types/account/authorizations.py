from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class Authorizations(TLObject):  # type: ignore
    __slots__: List[str] = ["authorization_ttl_days", "authorizations"]

    ID = 0x4bff8ea0
    QUALNAME = "types.account.Authorizations"

    def __init__(self, *, authorization_ttl_days: int, authorizations: List["raw.base.Authorization"]) -> None:
        self.authorization_ttl_days = authorization_ttl_days  # int
        self.authorizations = authorizations  # Vector<Authorization>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Authorizations":
        # No flags
        
        authorization_ttl_days = Int.read(b)
        
        authorizations = TLObject.read(b)
        
        return Authorizations(authorization_ttl_days=authorization_ttl_days, authorizations=authorizations)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.authorization_ttl_days))
        
        b.write(Vector(self.authorizations))
        
        return b.getvalue()
