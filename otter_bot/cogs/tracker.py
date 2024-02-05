
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

from otter_bot.sheet.sheet_manager import SheetManager
from otter_bot.functions.helper_functions import message_handler

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
        insertion_response = self.sheet_manager.insert_apply_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response))


    @Process.command()
    async def OA(self, ctx: Context, company: str) -> None:     
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_oa_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response, process_state='an Online Assessment'))


    @Process.command()
    async def Phone(self, ctx: Context, company: str) -> None:     
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_phone_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response, process_state='a Phone Interview'))
        
    

    @Process.command()
    async def Interview(self, ctx: Context, company: str) -> None:
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_interview_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response, process_state='a Interview'))
  


    @Process.command()
    async def Final_round(self, ctx: Context, company: str) -> None:
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_finalround_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response, process_state='a Final Round Interview'))

        


    @Process.command()
    async def Offer(self, ctx: Context, company: str) -> None:
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_offer_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response, process_state='an Offer', from_offer=True))

    
    @Process.command()
    async def Rejection(self, ctx: Context, company: str) -> None:
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_rejection_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response, process_state='a Rejection', from_rejection=True))



async def setup(bot: Bot) -> None:
    """Set up"""
    await bot.add_cog(Tracker(bot))
