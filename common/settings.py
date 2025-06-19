"""Чтение настроек из .env (python-dotenv)."""
import os
from aiohttp import BasicAuth
from dotenv import load_dotenv

load_dotenv()

TG_TOKEN       = os.getenv("TG_TOKEN")
DISCORD_TOKEN  = os.getenv("DISCORD_TOKEN")

VC_ID          = int(os.getenv("VC_ID", 0))

PROXY          = os.getenv("PROXY")          # URL вида http/https/socks5://host:port
PROXY_USER     = os.getenv("PROXY_USER")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")
PROXY_AUTH     = (BasicAuth(PROXY_USER, PROXY_PASSWORD)
                  if PROXY_USER and PROXY_PASSWORD else None)
