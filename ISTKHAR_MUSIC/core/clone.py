import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, Message

import config
from ISTKHAR_MUSIC.utils.decorators.language import language

# Yahan styled_button aur ButtonStyle import kiya gaya hai
from button import styled_button, ButtonStyle


# Main Bot Link (Where users can create a clone)
# Ideally, this should be in config, but hardcoding here works too.
BOT_LINK = "https://t.me/YTNAISHA_BOT"

# ✅ Helper to safely get Random Start Image
def get_random_start_img():
    if config.START_IMG_URL:
        if isinstance(config.START_IMG_URL, list):
            return random.choice(config.START_IMG_URL)
        return config.START_IMG_URL
    return "https://files.catbox.moe/wn3ool.jpg" # Fallback Image


@Client.on_message(filters.command("clone"))
@language
async def ping_clone(client: Client, message: Message, _):
    # ✅ Random Photo Logic (Spoiler Removed)
    await message.reply_photo(
        photo=get_random_start_img(),
        caption=_["NO_CLONE_MSG"],
        reply_markup=InlineKeyboardMarkup(
            [
                [styled_button("ɢᴏ ᴀɴᴅ ᴄʟᴏɴᴇ", url=BOT_LINK, style=ButtonStyle.SUCCESS)]
            ]
        )
    )
