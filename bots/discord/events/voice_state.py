import asyncio, time, logging
from discord.ext import commands
from common.state   import STATE
from common.settings import VC_ID
from bots.telegram.bot import tg_bot
from bots.telegram.keyboards.inline import main_keyboard
from bots.telegram.misc.text_builder import build_text

log = logging.getLogger(__name__)

AFK_TIMEOUT = 60          # секунд

def setup(bot: commands.Bot):

    async def refresh_message():
        if STATE.chat_id and STATE.message_id:
            text = await build_text(tg_bot, bot)
            await tg_bot.edit_message_text(
                text, chat_id=STATE.chat_id, message_id=STATE.message_id,
                reply_markup=main_keyboard(), parse_mode="MarkdownV2",
                disable_web_page_preview=True
            )

    @bot.event
    async def on_voice_state_update(member, before, after):
        uid = member.id

        # интересуют только тот самый канал
        ch_before = before.channel.id if before.channel else None
        ch_after  = after.channel.id  if after.channel  else None
        in_target = VC_ID in (ch_before, ch_after)
        if not in_target:
            return

        # ---- переходит / выходит из канала ----
        if ch_before != ch_after:
            STATE.muted_since.pop(uid, None)
            STATE.afk.discard(uid)
            await refresh_message()
            return

        # ---- mute / unmute ----
        if not before.self_mute and after.self_mute:          # ВКЛ mute
            STATE.muted_since[uid] = time.time()

            async def afk_checker(u=uid):
                await asyncio.sleep(AFK_TIMEOUT)
                if (
                    u in STATE.muted_since            # всё ещё замьючен
                    and (time.time() - STATE.muted_since[u]) >= AFK_TIMEOUT
                ):
                    STATE.afk.add(u)
                    await refresh_message()
            asyncio.create_task(afk_checker())

        elif before.self_mute and not after.self_mute:        # ВЫКЛ mute
            STATE.muted_since.pop(uid, None)
            if uid in STATE.afk:
                STATE.afk.remove(uid)
                await refresh_message()
