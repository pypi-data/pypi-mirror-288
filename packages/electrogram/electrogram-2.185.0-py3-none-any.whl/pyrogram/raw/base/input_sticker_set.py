from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputStickerSet = Union["raw.types.InputStickerSetAnimatedEmoji", "raw.types.InputStickerSetAnimatedEmojiAnimations", "raw.types.InputStickerSetDice", "raw.types.InputStickerSetEmojiChannelDefaultStatuses", "raw.types.InputStickerSetEmojiDefaultStatuses", "raw.types.InputStickerSetEmojiDefaultTopicIcons", "raw.types.InputStickerSetEmojiGenericAnimations", "raw.types.InputStickerSetEmpty", "raw.types.InputStickerSetID", "raw.types.InputStickerSetPremiumGifts", "raw.types.InputStickerSetShortName"]


# noinspection PyRedeclaration
class InputStickerSet:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputStickerSet"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
