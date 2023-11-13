
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
    async def oa(self, ctx: Context, company: str) -> None:
        
        discord_user = ctx.author.name 
        data_inserted_successfully = self.sheet_manager.insert_data(discord_user, company)

        if data_inserted_successfully:
            await ctx.send(f"{discord_user} has received an Online Assessment from {company}. ✅")

        else:
            await ctx.send(f"{discord_user} has already executed this command for the company: {company}. ❌")
        
    

    @commands.command()
    async def interviews(self, ctx: Context) -> None:
        pass


    @commands.command()
    async def final_round(self, ctx: Context) -> None:
        pass


    @commands.command()
    async def offer(self, ctx: Context) -> None:
        pass



async def setup(bot: Bot) -> None:
    """Set up"""
    await bot.add_cog(Tracker(bot))
