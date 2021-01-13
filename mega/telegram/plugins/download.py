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
        text=f"Link Generated Successfully \n\n <i> Copy and paste this link in your browser and the file download will start immediately </i> \n\n {emoji.LINK} : {file_link},
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text=f"{emoji.ROCKET} Direct Download Link {emoji.ROCKET}", url=file_link)],
              #  [InlineKeyboardButton(text=f"{emoji.PEN} Rename File",
               #                       callback_data=f"prflrn_{m.chat.id}_{m.message_id}")]
            ]
        )
    )


