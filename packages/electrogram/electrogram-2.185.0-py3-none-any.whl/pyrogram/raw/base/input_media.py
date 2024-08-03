from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputMedia = Union["raw.types.InputMediaContact", "raw.types.InputMediaDice", "raw.types.InputMediaDocument", "raw.types.InputMediaDocumentExternal", "raw.types.InputMediaEmpty", "raw.types.InputMediaGame", "raw.types.InputMediaGeoLive", "raw.types.InputMediaGeoPoint", "raw.types.InputMediaInvoice", "raw.types.InputMediaPaidMedia", "raw.types.InputMediaPhoto", "raw.types.InputMediaPhotoExternal", "raw.types.InputMediaPoll", "raw.types.InputMediaStory", "raw.types.InputMediaUploadedDocument", "raw.types.InputMediaUploadedPhoto", "raw.types.InputMediaVenue", "raw.types.InputMediaWebPage"]


# noinspection PyRedeclaration
class InputMedia:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputMedia"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
