from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ChatInviteAlready(TLObject):  # type: ignore
    __slots__: List[str] = ["chat"]

    ID = 0x5a686d7c
    QUALNAME = "types.ChatInviteAlready"

    def __init__(self, *, chat: "raw.base.Chat") -> None:
        self.chat = chat  # Chat

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatInviteAlready":
        # No flags
        
        chat = TLObject.read(b)
        
        return ChatInviteAlready(chat=chat)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.chat.write())
        
        return b.getvalue()
