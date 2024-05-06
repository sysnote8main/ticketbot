import discord
from discord.ext import commands
from discord import app_commands
from util.checker.user_check import is_owner
from constant.bot_settings import TEST_GUILD, COGS_FOLDER_NAME


class OwnerCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.check(is_owner)
    @app_commands.command(name="load_ext")
    @app_commands.describe(name="Cog's name")
    @app_commands.guilds(TEST_GUILD)
    async def _load_ext_cmd(self, ctx: discord.Interaction, name: str):
        await ctx.response.defer()
        cog_name = f"{COGS_FOLDER_NAME}.{name}"
        try:
            load_type = "load"
            if cog_name in self.bot.extensions.keys():
                await self.bot.reload_extension(cog_name)
                load_type = "reload"
            else:
                await self.bot.load_extension(cog_name)
            await ctx.followup.send(f"Successfully to {load_type} extension. (ext:{cog_name})", ephemeral=True)
        except commands.ExtensionFailed as e:
            print(f"[Error] Failed to load extension.\n{e.__traceback__}")
            await ctx.followup.send(f"Failed to {load_type} extension. (ext:{cog_name})\n```{e.__traceback__}```")

    @commands.check(is_owner)
    @app_commands.command(name="unload_ext")
    @app_commands.describe(name="Cog's name")
    @app_commands.guilds(TEST_GUILD)
    async def _unload_ext_cmd(self, ctx: discord.Interaction, name: str):
        await ctx.response.defer()
        cog_name = f"{COGS_FOLDER_NAME}.{name}"
        try:
            if cog_name in self.bot.extensions.keys():
                await self.bot.unload_extension(cog_name)
                await ctx.followup.send(f"Successfully to unload extension. (ext:{cog_name})", ephemeral=True)
            else:
                await ctx.followup.send(f"This extension wasn't loaded! (ext:{cog_name})")
        except commands.ExtensionFailed as e:
            print(f"[Error] Failed to unload extension.\n{e}")
            await ctx.followup.send(f"Failed to unload extension. (ext:{cog_name})\n```{e}```")

async def setup(bot: commands.Bot):
    await bot.add_cog(OwnerCog(bot))