from pathlib import Path
import discord
from discord.ext import commands
from constant.environ import TOKEN, PREFIX
from constant.bot_settings import INTENTS, DEBUG_MODE, TEST_GUILD, COGS_FOLDER_NAME
import util.database as database

disabled_cog = [
    "dice"
]

class TicketBot(commands.Bot):
    async def setup_hook(self) -> None:
        for cog in Path(COGS_FOLDER_NAME).glob("**/*.py"):
            if cog.stem == "__init__" or cog.stem in disabled_cog:
                continue
            try:
                p = cog.relative_to(".").with_suffix("").as_posix().replace("/", ".")
                await self.load_extension(p)
                print(f"[Extension] {p} Loaded!")
            except commands.ExtensionFailed as e:
                print(f"[ERROR] Failed to load extension. (ext:{p})")
        if DEBUG_MODE:
            await self.tree.sync(guild=TEST_GUILD)
        else:
            await self.tree.sync()

    async def on_ready(self):
        print(f"Bot on ready with {self.user.display_name}")
        print(f"Caching database...")
        await database.cache_counts()
        print(f"Finished to cache database!")

    async def on_command_error(ctx: commands.Context, error):
        if ctx.author.bot:
            return
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send(
                "このコマンドは存在していないか、権限不足のため使用することができません。",
                ephemeral=True,
            )

bot: commands.Bot = TicketBot(
    command_prefix=PREFIX,
    intents=INTENTS
)

bot.run(token=TOKEN)
