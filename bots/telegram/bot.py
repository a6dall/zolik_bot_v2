import importlib
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, Router

from common.settings import TG_TOKEN, PROXY
from common.logging import setup as setup_logging

# прокси через env
if PROXY:
    os.environ["http_proxy"]  = PROXY
    os.environ["https_proxy"] = PROXY

log = logging.getLogger(__name__)

tg_bot = Bot(token=TG_TOKEN)
dp     = Dispatcher()
router = Router()
dp.include_router(router)

# ---------- динамическая регистрация хендлеров ----------
def _autoload_handlers():
    pkg = "bots.telegram.handlers"
    handlers_path = Path(__file__).with_name("handlers")
    for file in handlers_path.glob("*.py"):
        if file.name.startswith("_"):     # пропускаем __init__.py
            continue
        mod = importlib.import_module(f"{pkg}.{file.stem}")
        if hasattr(mod, "register"):
            mod.register(router)
            log.debug("registered tg handler: %s", file.stem)

_autoload_handlers()
# --------------------------------------------------------

async def start_telegram_bot():
    setup_logging()
    log.info("Starting Telegram polling")
    await dp.start_polling(tg_bot)
