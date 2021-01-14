from pyrogram import filters, emoji, Client
#from pyrogram.types import Message
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ForceReply

from mega.database.files import MegaFiles
from mega.database.users import MegaUsers
from ...telegram import Common


@Client.on_message(filters.command("start", prefixes=["/"]))
async def start_message_handler(c: Client, m: Message):
    await MegaUsers().insert_user(m.from_user.id)
    if len(m.command) > 1:
        if m.command[1].split("-")[0] == 'plf':
            file_id = m.command[1].split("-", 1)[1]
            file_details = await MegaFiles().get_file_by_file_id(file_id)

            if file_details is not None:
                file_message = await c.get_messages(
                    chat_id=file_details['chat_id'],
                    message_ids=file_details['msg_id']
                )

                if str(file_details['file_type'].split("/"))[0].lower() == "video":
                    await m.reply_video(
                        video=file_message.video.file_id,
                        file_ref=file_message.video.file_ref
                    )
                elif str(file_details['file_type'].split("/"))[0].lower() == "audio":
                    await m.reply_audio(
                        audio=file_message.audio.file_id,
                        file_ref=file_message.audio.file_ref
                    )
                else:
                    await m.reply_document(
                        document=file_message.document.file_id,
                        file_ref=file_message.document.file_ref
                    )
    else:
        await m.reply_text(
            text=f"""Hello!!
I am Public link generator bot.

<b>I can generate Direct URL of any Telegram Medias sent to me...</b>

☛ Send Me A Telegram file To get Direct link

""",
            reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=f"⚜ Updates Channel ⚜", url='https://t.me/MyTestBotZ')],
                [InlineKeyboardButton(text=f"🧞‍♂ Creator",url='https://t.me/OO7ROBot')]
              #  [InlineKeyboardButton(text=f"{emoji.PEN} Rename File",
               #                       callback_data=f"prflrn_{m.chat.id}_{m.message_id}")]
            ]
        )
        )


@Client.on_message(group=-1)
async def stop_user_from_doing_anything(_, message: Message):
    allowed_users = Common().allowed_users
    if allowed_users and message.from_user.id not in allowed_users:
    #    message.stop_propagation()
    #else:
        message.continue_propagation()
