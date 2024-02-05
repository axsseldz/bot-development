from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

from otter_bot.sheet.sheet_manager import SheetManager
from otter_bot.functions.helper_functions import message_handler
from otter_bot.cogs.views.add_company import ButtonAddCompany

class Company(commands.Cog):
    """Companies"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.sheet_manager = SheetManager()

    @commands.group(
        brief = "Add companies to follow processes",
        invoke_without_command=True,
        pass_context=True
    )
    async def company(self, ctx: Context) -> None:
        await ctx.send_help(ctx.command)

    @company.command()
    async def add(self, ctx: Context) -> None:
        
        view = ButtonAddCompany(timeout=10)
        message = await ctx.send(view=view)
        view.message = message
        

async def setup(bot: Bot) -> None:
    """Set up"""
    await bot.add_cog(Company(bot))