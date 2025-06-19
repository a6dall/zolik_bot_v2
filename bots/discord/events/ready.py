import logging
from discord.ext import commands

log = logging.getLogger(__name__)

def setup(bot: commands.Bot):
    @bot.event
    async def on_ready():
        log.info("Discord ready as %s (ID %s)", bot.user, bot.user.id)
        for guild in bot.guilds:
            await guild.chunk()
