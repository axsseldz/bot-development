
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context, MissingRequiredArgument, CommandError, CommandNotFound

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
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_apply_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response))


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
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_oa_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response, process_state='an Online Assessment'))


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
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_phone_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response, process_state='a Phone Interview'))
        
    

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
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_interview_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response, process_state='a Interview'))
  


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
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_finalround_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response, process_state='a Final Round Interview'))

        


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
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_offer_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response, process_state='an Offer', from_offer=True))

    
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
        discord_user = ctx.author.name 
        insertion_response = self.sheet_manager.insert_rejection_data(discord_user, company)

        await ctx.send(message_handler(discord_user, company, insertion_response, process_state='a Rejection', from_rejection=True))


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
