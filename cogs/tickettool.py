import discord
from discord import app_commands
from discord.ext import commands
from constant.bot_settings import TEST_GUILD
from constant.cog.tickettool_settings import EVERYONE_PERM, SENDER_PERM
import util.database as database

class TicketToolCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot.add_view(TicketOpenButton())
        self.bot.add_view(TicketCloseButton())

    @app_commands.command(name="ticket_setup", description="Setup ticket system")
    @app_commands.guilds(TEST_GUILD)
    @app_commands.guild_only()
    async def _ticket_tool_setup(self, interaction: discord.Interaction):
        if not interaction.user.resolved_permissions.administrator:
            await interaction.response.send_message("このコマンドを実行するには管理者権限が必要です。", ephemeral=True)
            return
        await interaction.response.send_message("Successfully to setup ticket button!", ephemeral=True)
        embed = discord.Embed(title="Support Ticket", description="Click below button to open ticket!")
        await interaction.channel.send(embed=embed,view=TicketOpenButton())

class TicketCloseButton(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close ticket",
        style=discord.ButtonStyle.success,
        custom_id="ticket_tool:close"
    )
    async def _ticket_close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.channel.set_permissions(interaction.user, send_messages=False)
        await interaction.channel.send("Closed by " + interaction.user.mention)

class TicketOpenButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Open your channel.",
        style=discord.ButtonStyle.primary,
        custom_id="ticket_tool:open"
    )
    async def _ticket_open_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        count = database.get_counts(interaction.channel_id) + 1

        # Channel setup
        channel = await interaction.channel.category.create_text_channel(f"Ticket-{count:04}")
        await channel.set_permissions(channel.guild.default_role, overwrite=EVERYONE_PERM)
        await channel.set_permissions(interaction.user, overwrite=SENDER_PERM)
        await channel.send(view=TicketCloseButton())

        await interaction.response.send_message(f"Ticket opened at {channel.jump_url}", ephemeral=True)

        # update count
        await database.set_counts(interaction.channel_id, count)

async def setup(bot: commands.Bot):
    await bot.add_cog(TicketToolCog(bot))