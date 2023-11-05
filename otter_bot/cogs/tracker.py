
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context



class Tracker(commands.Cog):
    """Tracker"""

    def __init__(self, bot: Bot):
        self.bot: Bot = bot
    

    @commands.command()
    async def tracker(self, ctx: Context) -> None:
        """Command"""

        await ctx.send("this is a tracker command!")



async def setup(bot: Bot) -> None:
    """Set up"""
    await bot.add_cog(Tracker(bot))
