import asyncio
from bots.telegram.bot import start_telegram_bot
from bots.discord.bot  import start_discord_bot
from common.logging    import setup as setup_logging

setup_logging()

async def main():
    await asyncio.gather(
        start_telegram_bot(),
        start_discord_bot(),
    )

if __name__ == "__main__":
    asyncio.run(main())
