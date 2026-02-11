from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup
from config import START_IMG_URL, SUPPORT_CHAT


@Client.on_chat_member_updated(filters.group)
async def welcome_handler(client: Client, update: ChatMemberUpdated):
    if update.new_chat_member and not update.old_chat_member:
        user = update.new_chat_member.user
        if user.is_bot:
            return

        text = (
            f"✨ **Welcome {user.mention}!** ✨\n\n"
            f"🎶 Is group me music ka maza lo\n"
            f"📌 Rules follow karo\n"
            f"❤️ Enjoy & stay active!"
        )

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💬 Support", url=SUPPORT_CHAT
                    )
                ]
            ]
        )

        await client.send_photo(
            chat_id=update.chat.id,
            photo=START_IMG_URL,
            caption=text,
            reply_markup=buttons
        )
