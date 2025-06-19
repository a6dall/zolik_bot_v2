import importlib
import logging
from pathlib import Path

import discord
from discord.ext import commands

from common.settings import DISCORD_TOKEN, PROXY, PROXY_AUTH
from common.logging import setup as setup_logging

log = logging.getLogger(__name__)

_intents = discord.Intents.default()
_intents.guilds       = True
_intents.members      = True
_intents.voice_states = True

d_bot = commands.Bot(
    command_prefix="!",
    intents=_intents,
    proxy=PROXY,
    proxy_auth=PROXY_AUTH,
)

def get_discord_bot() -> commands.Bot:
    return d_bot

# автозагрузка events
def _autoload_events():
    pkg = "bots.discord.events"
    events_path = Path(__file__).with_name("events")
    for file in events_path.glob("*.py"):
        if file.name.startswith("_"):
            continue
        mod = importlib.import_module(f"{pkg}.{file.stem}")
        if hasattr(mod, "setup"):
            mod.setup(d_bot)
            log.debug("registered discord event: %s", file.stem)

_autoload_events()

async def start_discord_bot():
    setup_logging()
    await d_bot.start(DISCORD_TOKEN)
