import os

# TODO remove when build docker
from dotenv import load_dotenv

load_dotenv()


def send_failed_message_and_exit(name: str):
    print(f"[Error][System] Failed to load {name}.")
    exit(1)


def get_env_or_exit(name: str):
    return os.getenv(name) or send_failed_message_and_exit(name)


PREFIX = get_env_or_exit("BOT_PREFIX")

TOKEN = get_env_or_exit("BOT_TOKEN")

BOT_OWNER_ID = get_env_or_exit("BOT_OWNER_ID")

BOT_GUILD_ID = get_env_or_exit("BOT_GUILD_ID")

MONGO_URL = get_env_or_exit("MONGO_URL")