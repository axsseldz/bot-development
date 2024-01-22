
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

from otter_bot.sheet.sheet_manager import SheetManager

class Tracker(commands.Cog):
    """Tracker"""

    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.sheet_manager = SheetManager()


    @commands.group(
        brief="Tracker Bot Commands",
        invoke_without_command=True,
        pass_context=True,
    )
    async def Process(self, ctx: Context) -> None:
        await ctx.send_help(ctx.command)


    @Process.command()
    async def Apply(self, ctx: Context, company: str) -> None:     
        discord_user = ctx.author.name 
        data_inserted_successfully = self.sheet_manager.insert_apply_data(discord_user, company)

        if data_inserted_successfully:
            await ctx.send(f"{discord_user} has applied to {company}. ✅")

        else:
            await ctx.send("ERROR... ❌")


    @Process.command()
    async def OA(self, ctx: Context, company: str) -> None:     
        discord_user = ctx.author.name 
        data_inserted_successfully = self.sheet_manager.insert_oa_data(discord_user, company)

        if data_inserted_successfully:
            await ctx.send(f"{discord_user} has received an Online Assessment from {company}. ✅")

        else:
            await ctx.send("ERROR... ❌")


    @Process.command()
    async def Phone(self, ctx: Context, company: str) -> None:     
        discord_user = ctx.author.name 
        data_inserted_successfully = self.sheet_manager.insert_phone_data(discord_user, company)

        if data_inserted_successfully:
            await ctx.send(f"{discord_user} has received a Phone Interview from {company}. ✅")

        else:
            await ctx.send("ERROR... ❌")
        
    

    @Process.command()
    async def Interview(self, ctx: Context, company: str) -> None:
        discord_user = ctx.author.name 
        data_inserted_successfully = self.sheet_manager.insert_interview_data(discord_user, company)

        if data_inserted_successfully:
            await ctx.send(f"{discord_user} has received an Interview from {company}. ✅")

        elif data_inserted_successfully == False:
            await ctx.send("ERROR... ❌")
  


    @Process.command()
    async def Final_round(self, ctx: Context, company: str) -> None:
        discord_user = ctx.author.name 
        data_inserted_successfully = self.sheet_manager.insert_finalround_data(discord_user, company)

        if data_inserted_successfully:
            await ctx.send(f"{discord_user} has received a Final Round Interview from {company}. ✅")

        elif data_inserted_successfully == False:
            await ctx.send("ERROR... ❌")


    @Process.command()
    async def Offer(self, ctx: Context, company: str) -> None:
        discord_user = ctx.author.name 
        data_inserted_successfully = self.sheet_manager.insert_offer_data(discord_user, company)

        if data_inserted_successfully:
            await ctx.send(f"{discord_user} has received an Offer from {company}. 🎉")

        elif data_inserted_successfully == False:
            await ctx.send("ERROR... ❌")

    
    @Process.command()
    async def Rejection(self, ctx: Context, company: str) -> None:
        discord_user = ctx.author.name 
        data_inserted_successfully = self.sheet_manager.insert_rejection_data(discord_user, company)

        if data_inserted_successfully:
            await ctx.send(f"{discord_user} has been rejected from {company}. 😭")

        elif data_inserted_successfully == False:
            await ctx.send("ERROR... ❌")



async def setup(bot: Bot) -> None:
    """Set up"""
    await bot.add_cog(Tracker(bot))
