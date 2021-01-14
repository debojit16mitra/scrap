import os
import re
import secrets
import asyncio
import logging
import tldextract
import humanfriendly as size
from mega.common import Common
from pyrogram import emoji, Client
from mega.helpers.ytdl import YTdl
from mega.helpers.screens import Screens
from mega.database.files import MegaFiles
from mega.database.users import MegaUsers
from mega.helpers.seerd_api import SeedrAPI
from pyrogram.errors import MessageNotModified
from mega.helpers.media_info import MediaInfo
from mega.helpers.uploader import UploadFiles
from mega.helpers.downloader import Downloader
from mega.telegram.utils.custom_download import TGCustomYield
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ForceReply

from ..utils import filters

youtube_dl_links = ["youtube", "youtu", "facebook", "soundcloud"]





@Client.on_message(filters.private & (filters.document | filters.video | filters.audio), group=4)
async def media_receive_handler(c: Client, m: Message):
    user_settings = await MegaUsers().get_user(m.from_user.id)
    if "f_rename_type" not in user_settings:
        await MegaUsers().update_file_rename_settings(m.from_user.id, "disk")

    fd_msg = await m.forward(
        chat_id=Common().bot_dustbin
    )

    file_link = f"https://{Common().web_fqdn}/{fd_msg.message_id}" if Common().on_heroku else \
        f"http://{Common().web_fqdn}:{Common().web_port}/{fd_msg.message_id}"

    await m.reply_text(
        text=f"""<b>Direct Link Generated Successfully</b> \n\n <i>Copy and Paste this Link in your Browser and the File Download will Start Immediately </i> \n\n {emoji.LINK} <b>#Link</b> : <code> {file_link} </code> \n\n\n ✪༺ ──•◈•── ──•◈•──༻✪  \n Thanks For Using <b> @Link4FilesBot </b> """,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=f"{emoji.ROCKET} Direct Download Link {emoji.ROCKET}", url=file_link)],
                #[InlineKeyboardButton(text=f"🎗️ ѕнαяє🎗️ ѕυρρσят 🎗", url='https://tg://msg?text=Hey%20Broh%F0%9F%A5%B0%2C%0AThis%20Bot%20Generate%20Instant%20File%20Direct%20Download%20Link%F0%9F%94%A5%0A%0ABot%20Link%20%3A-%20%40LiNk4filesbot')]
                #  [InlineKeyboardButton(text=f"{emoji.PEN} Rename File",
               #                       callback_data=f"prflrn_{m.chat.id}_{m.message_id}")]
            ]
        )
    )


