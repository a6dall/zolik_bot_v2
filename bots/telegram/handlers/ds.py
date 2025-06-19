import logging
from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command        # ⬅️ НОВЫЙ импорт!

from bots.telegram.keyboards.inline import main_keyboard
from bots.telegram.misc.text_builder import build_text
from common.state import STATE
from bots.discord.bot import get_discord_bot

log = logging.getLogger(__name__)

def register(router: Router):

    @router.message(Command("ds"))         # ⬅️ вместо commands=["ds"]
    async def ds_handler(msg: types.Message):
        log.info("Received /ds from %s", msg.from_user.id)
        await get_discord_bot().wait_until_ready()

        # reset …
        STATE.chat_id     = msg.chat.id
        STATE.message_id  = None
        STATE.caller_id   = msg.from_user.id
        STATE.caller_name = msg.from_user.full_name
        STATE.coming.clear()
        STATE.busy.clear()

        text = await build_text(msg.bot)
        sent = await msg.answer(
            text,
            reply_markup=main_keyboard(),
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview=True,
        )
        STATE.message_id = sent.message_id
        log.info("Sent /ds message id=%s", sent.message_id)
