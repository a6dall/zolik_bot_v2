import logging
from aiogram import types
from aiogram.enums import ParseMode
from bots.telegram.misc.text_builder import escape_md
from aiogram.exceptions import TelegramBadRequest

from bots.telegram.keyboards.inline import main_keyboard
from bots.telegram.misc.text_builder import build_text
from common.state import STATE

log = logging.getLogger(__name__)

def register(router):
    @router.callback_query(lambda c: c.data in ("coming", "busy"))
    async def cb_handler(query: types.CallbackQuery):
        who_name = escape_md(query.from_user.full_name)
        who_md   = f"[{who_name}](tg://user?id={query.from_user.id})"

        if query.data == "coming":
            STATE.coming.add(who_md)
            STATE.busy.discard(who_md)
        else:
            STATE.busy.add(who_md)
            STATE.coming.discard(who_md)

        text = await build_text(query.bot)
        try:
            await query.bot.edit_message_text(
                text,
                chat_id=STATE.chat_id,
                message_id=STATE.message_id,
                reply_markup=main_keyboard(),
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True,
            )
        except TelegramBadRequest:
            pass

        await query.answer()
        log.info("Updated list after %s", query.data)
