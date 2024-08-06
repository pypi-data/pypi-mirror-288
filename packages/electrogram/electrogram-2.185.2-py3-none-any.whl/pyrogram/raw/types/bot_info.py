from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class BotInfo(TLObject):  # type: ignore
    __slots__: List[str] = ["has_preview_medias", "user_id", "description", "description_photo", "description_document", "commands", "menu_button"]

    ID = 0x8f300b57
    QUALNAME = "types.BotInfo"

    def __init__(self, *, has_preview_medias: Optional[bool] = None, user_id: Optional[int] = None, description: Optional[str] = None, description_photo: "raw.base.Photo" = None, description_document: "raw.base.Document" = None, commands: Optional[List["raw.base.BotCommand"]] = None, menu_button: "raw.base.BotMenuButton" = None) -> None:
        self.has_preview_medias = has_preview_medias  # flags.6?true
        self.user_id = user_id  # flags.0?long
        self.description = description  # flags.1?string
        self.description_photo = description_photo  # flags.4?Photo
        self.description_document = description_document  # flags.5?Document
        self.commands = commands  # flags.2?Vector<BotCommand>
        self.menu_button = menu_button  # flags.3?BotMenuButton

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BotInfo":
        
        flags = Int.read(b)
        
        has_preview_medias = True if flags & (1 << 6) else False
        user_id = Long.read(b) if flags & (1 << 0) else None
        description = String.read(b) if flags & (1 << 1) else None
        description_photo = TLObject.read(b) if flags & (1 << 4) else None
        
        description_document = TLObject.read(b) if flags & (1 << 5) else None
        
        commands = TLObject.read(b) if flags & (1 << 2) else []
        
        menu_button = TLObject.read(b) if flags & (1 << 3) else None
        
        return BotInfo(has_preview_medias=has_preview_medias, user_id=user_id, description=description, description_photo=description_photo, description_document=description_document, commands=commands, menu_button=menu_button)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 6) if self.has_preview_medias else 0
        flags |= (1 << 0) if self.user_id is not None else 0
        flags |= (1 << 1) if self.description is not None else 0
        flags |= (1 << 4) if self.description_photo is not None else 0
        flags |= (1 << 5) if self.description_document is not None else 0
        flags |= (1 << 2) if self.commands else 0
        flags |= (1 << 3) if self.menu_button is not None else 0
        b.write(Int(flags))
        
        if self.user_id is not None:
            b.write(Long(self.user_id))
        
        if self.description is not None:
            b.write(String(self.description))
        
        if self.description_photo is not None:
            b.write(self.description_photo.write())
        
        if self.description_document is not None:
            b.write(self.description_document.write())
        
        if self.commands is not None:
            b.write(Vector(self.commands))
        
        if self.menu_button is not None:
            b.write(self.menu_button.write())
        
        return b.getvalue()
