
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

from otter_bot.sheet.sheet_manager import SheetManager

class Tracker(commands.Cog):
    """Tracker"""

    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.sheet_manager = SheetManager()

    @commands.command()
    async def tracker(self, ctx: Context) -> None:
        """Command"""
        response1 = self.sheet_manager.query('A1:F4')
        print(response1)
        await ctx.send("this is a tracker command!")

async def setup(bot: Bot) -> None:
    """Set up"""
    await bot.add_cog(Tracker(bot))
