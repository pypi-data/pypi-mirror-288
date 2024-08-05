from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputFileLocation = Union["raw.types.InputDocumentFileLocation", "raw.types.InputEncryptedFileLocation", "raw.types.InputFileLocation", "raw.types.InputGroupCallStream", "raw.types.InputPeerPhotoFileLocation", "raw.types.InputPhotoFileLocation", "raw.types.InputPhotoLegacyFileLocation", "raw.types.InputSecureFileLocation", "raw.types.InputStickerSetThumb", "raw.types.InputTakeoutFileLocation"]


# noinspection PyRedeclaration
class InputFileLocation:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputFileLocation"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
