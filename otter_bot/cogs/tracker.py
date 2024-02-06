import os

from discord import utils
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context, MissingRequiredArgument, CommandError, CommandNotFound

from otter_bot.sheet.sheet_manager import SheetManager
from otter_bot.cogs.views.add_company import ButtonAddCompany
from otter_bot.functions.helper_functions import message_handler
from otter_bot.common.constants import SUDO_CHANNEL_ID
from otter_bot.functions.helper_functions import get_channel_by_id

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
        """Main command group for job application tracking."""
        await ctx.send_help(ctx.command)


    @Process.command()
    async def Apply(self, ctx: Context, company: str) -> None:    
        """
        Record the application process for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process Apply [company]

        Example:
        !Process Apply Google
        """
        current_channel = ctx.channel
        company_str: str = "".join(company)
        companies = self.sheet_manager.get_allowed_companies()

        if [company_str] not in companies:
            await current_channel.send(f"**{company_str}** is not registered, try to request to add this company first. 📋")
            return 

        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_apply_data(discord_user, company)
        await current_channel.send(message_handler(discord_user, company, insertion_response))


    @Process.command()
    async def OA(self, ctx: Context, company: str) -> None: 
        """
        Record the Online Assessment (OA) stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process OA [company]

        Example:
        !Process OA Google
        """  
        current_channel = ctx.channel
        company_str: str = "".join(company)
        companies = self.sheet_manager.get_allowed_companies()

        if [company_str] not in companies:
            await current_channel.send(f"**{company_str}** is not registered, try to request to add this company first. 📋")
            return 

        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_oa_data(discord_user, company)

        await current_channel.send(message_handler(discord_user, company, insertion_response, process_state='an Online Assessment'))


    @Process.command()
    async def Phone(self, ctx: Context, company: str) -> None:     
        """
        Record the Phone Interview (Phone) stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process Phone [company]

        Example:
        !Process Phone Google
        """    
        current_channel = ctx.channel
        company_str: str = "".join(company)
        companies = self.sheet_manager.get_allowed_companies()

        if [company_str] not in companies:
            await current_channel.send(f"**{company_str}** is not registered, try to request to add this company first. 📋")
            return 
        
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_phone_data(discord_user, company)

        await current_channel.send(message_handler(discord_user, company, insertion_response, process_state='a Phone Interview'))
        
    

    @Process.command()
    async def Interview(self, ctx: Context, company: str) -> None:
        """
        Record the Interview stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process Interview [company]

        Example:
        !Process Interview Google
        """    
        current_channel = ctx.channel
        company_str: str = "".join(company)
        companies = self.sheet_manager.get_allowed_companies()

        if [company_str] not in companies:
            await current_channel.send(f"**{company_str}** is not registered, try to request to add this company first. 📋")
            return
        
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_interview_data(discord_user, company)

        await current_channel.send(message_handler(discord_user, company, insertion_response, process_state='a Interview'))
  


    @Process.command()
    async def Final_round(self, ctx: Context, company: str) -> None:
        """
        Record the Final Round stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process Final_round [company]

        Example:
        !Process Final_round Google
        """    
        current_channel = ctx.channel
        company_str: str = "".join(company)
        companies = self.sheet_manager.get_allowed_companies()

        if [company_str] not in companies:
            await current_channel.send(f"**{company_str}** is not registered, try to request to add this company first. 📋")
            return
        
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_finalround_data(discord_user, company)

        await current_channel.send(message_handler(discord_user, company, insertion_response, process_state='a Final Round Interview'))

        


    @Process.command()
    async def Offer(self, ctx: Context, company: str) -> None:
        """
        Record the Offer stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process Offer [company]

        Example:
        !Process Offer Google
        """    
        current_channel = ctx.channel
        company_str: str = "".join(company)
        companies = self.sheet_manager.get_allowed_companies()

        if [company_str] not in companies:
            await current_channel.send(f"**{company_str}** is not registered, try to request to add this company first. 📋")
            return
        
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_offer_data(discord_user, company)

        await current_channel.send(message_handler(discord_user, company, insertion_response, process_state='an Offer', from_offer=True))

    
    @Process.command()
    async def Rejection(self, ctx: Context, company: str) -> None:
        """
        Record the Rejection stage for a specific company.

        Parameters:
        - company (str): The name of the company.

        Usage:
        !Process Rejection [company]

        Example:
        !Process Rejection Google
        """    
        current_channel = ctx.channel
        company_str: str = "".join(company)
        companies = self.sheet_manager.get_allowed_companies()

        if [company_str] not in companies:
            await current_channel.send(f"**{company_str}** is not registered, try to request to add this company first. 📋")
            return
        
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_rejection_data(discord_user, company)

        await current_channel.send(message_handler(discord_user, company, insertion_response, process_state='a Rejection', from_rejection=True))

    @Process.command()
    async def Add(self, ctx: Context, *company: str) -> None:
        # get the channel where command was called and send message
        current_channel = ctx.channel
        discord_user = ctx.author.name 
        company_str: str = "".join(company)
        channel_id: int = SUDO_CHANNEL_ID
        channel = get_channel_by_id(self.bot, channel_id)
        companies = self.sheet_manager.get_allowed_companies()

        if [company_str] in companies:
            await current_channel.send(f"**{company_str}** has been added before, please check our companies list. 📋")
            return 
            
        
        await current_channel.send(f"Request for approval has been submitted to the administration channel to include **{company_str}** in our portfolio. ⌛") 
        await channel.send(f"Incoming pending approval to include **{company_str}** in our companies portfolio. ⌛")

        view = ButtonAddCompany(timeout=36000)
        message = await channel.send(view=view)
        view.message = message
        await view.wait()

        if view.response:
            #update spread sheet
            response = self.sheet_manager.insert_company_data(company_str)

            if response:
                await current_channel.send(f"A new company!!, **{company_str}** has been added to our companies portfolio. 🤩")
                await ctx.author.send(f'Congrats! {discord_user}, your request to include **{company_str}** in our portfolio has been approved ✅')

        else:
            await ctx.author.send(f'Sorry, your request to include **{company_str}** in our companies portfolio has been rejected, check our guinelines or reach out one of our *ROOT* members, thank you. 📋')
            await ctx.current_channel.send(f"Request to include **{company_str}** in our companies portfolio has been rejected, check our guinelines or reach out one of our *ROOT* members, thank you. 📋")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        """
        Handle errors occurring during command execution.

        Parameters:
        - ctx (Context): The command context.
        - error (CommandError): The error that occurred.
        """
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Error: Missing required argument '{error.param.name}' for the command '{ctx.command.qualified_name}'. ⚙️")
            
        elif isinstance(error, CommandNotFound):
            await ctx.send(f"Error: Command not found. Please check the command syntax and try again. 📋")

        else:
            # Handle other errors or log them as needed
            print(f"An error occurred: {type(error).__name__}: {str(error)}")

async def setup(bot: Bot) -> None:
    """Set up"""
    await bot.add_cog(Tracker(bot))
