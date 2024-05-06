import discord
from discord.ext import commands
from discord import app_commands
from constant.bot_settings import TEST_GUILD

import random

class DiceCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def roll_dices(self, count: int, faces: int) -> list[int]:
        return [random.randint(1, faces) for _ in range(count)]

    @app_commands.command(name="dice", description="ダイスを振ります")
    @app_commands.describe(count="回数", faces="面の数")
    @app_commands.guilds(TEST_GUILD)
    async def _dice_cmd(self, ctx: discord.Interaction, count: app_commands.Range[int, 1, 100], faces: app_commands.Range[int, 1, 10000]):
        rolls = self.roll_dices(count, faces)
        rolls_str = ", ".join(list(map(str, rolls)))
        output = [
            f"あなたは、{faces}面ダイスを{count}回振りました。",
            f"出目: {rolls_str}",
            f"合計: {sum(rolls)}"
        ]
        await ctx.response.send_message("\n".join(output))

async def setup(bot: commands.Bot):
    await bot.add_cog(DiceCog(bot))