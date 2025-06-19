import re
from typing import Optional
from common.state import STATE
from common.settings import VC_ID

_MD_V2_SPECIALS = r"_*[\]()~`>#+-=|{}.!"

def escape_md(text: str) -> str:
    """
    Экранирует все спец-символы MarkdownV2.
    Используйте вместо устаревшего aiogram.utils.markdown.escape_md.
    """
    return re.sub(f"([{re.escape(_MD_V2_SPECIALS)}])", r"\\\1", text)

async def build_text(tg_bot, d_bot: Optional["commands.Bot"] = None) -> str:
    """
    Собирает Markdown-текст.
    tg_bot — экземпляр Telegram-бота.
    d_bot  — (опц.) экземпляр Discord-клиента, если уже есть.
    """
    if d_bot is None:
        from bots.discord.bot import get_discord_bot
        d_bot = get_discord_bot()

    caller_md = (
        f"[{escape_md(STATE.caller_name)}](tg://user?id={STATE.caller_id})"
        if STATE.caller_id else escape_md("—")
    )

    vc = d_bot.get_channel(VC_ID) if d_bot else None
    chan_name = escape_md(vc.name) if vc else escape_md("—")
    voice_list = "\n".join(
        f"• {escape_md(m.display_name)}{' (AFK)' if m.id in STATE.afk else ''}"
        for m in (vc.members if vc else [])
    ) or escape_md("никого")

    coming = "\n".join(STATE.coming) or escape_md("никого")
    busy   = "\n".join(STATE.busy)   or escape_md("никого")

    admins = await tg_bot.get_chat_administrators(STATE.chat_id) if STATE.chat_id else []
    admins_md = " ".join(
        f"[{escape_md(a.user.full_name)}](tg://user?id={a.user.id})"
        for a in admins
    ) or escape_md("никого")

    return (
        f"{caller_md} зовёт всех\\!\n\n"
        f"*Уже в дискорде\\:*\n"
        f"```{chan_name}\n{voice_list}\n```\n"
        f"*✅ Придут* \\({len(STATE.coming)}\\)\\:\n{coming}\n\n"
        f"*❌ Заняты* \\({len(STATE.busy)}\\)\\:\n{busy}\n\n"
        f"{admins_md}"
    )
