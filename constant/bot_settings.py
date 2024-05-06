import discord
from constant.environ import BOT_GUILD_ID

DEBUG_MODE: bool = True # TODO need to change for deploy

INTENTS = discord.Intents.default()
INTENTS.messages = True
INTENTS.guild_messages = True
INTENTS.message_content = True

TEST_GUILD = discord.Object(id=BOT_GUILD_ID)

COGS_FOLDER_NAME = "cogs"