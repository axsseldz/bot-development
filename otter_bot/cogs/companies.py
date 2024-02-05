import os

from dotenv import load_dotenv

from discord import utils
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

from otter_bot.sheet.sheet_manager import SheetManager
from otter_bot.functions.helper_functions import message_handler
from otter_bot.cogs.views.add_company import ButtonAddCompany

load_dotenv()

class Company(commands.Cog):
    """Companies"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.sheet_manager = SheetManager()

    @commands.group(
        brief = 'Add companies to follow processes',
        invoke_without_command=True,
        pass_context=True
    )
    async def company(self, ctx: Context) -> None:
        await ctx.send_help(ctx.command)

    @company.command()
    async def add(self, ctx: Context, company_name: str) -> None:
        # get the channel where command was called and send message
        current_channel = ctx.channel
        
        await current_channel.send(f'Approval sent for **{company_name}** company ⌛') 
        
        # Identify staff channel and send approval message
        staff_channel_name = os.environ['APPROVAL_CHANNEL_NAME']
        staff_channel = utils.get(ctx.guild.channels, name=staff_channel_name)
        staff_channel = staff_channel if staff_channel else current_channel

        await staff_channel.send(f'Incoming pending approval for **{company_name}** company ⌛')
        view = ButtonAddCompany(timeout=10)
        message = await staff_channel.send(view=view)
        view.message = message
        await view.wait()

        if view.response:
            #update spread sheet
            await ctx.author.send(f'Congrats, your request to add **{company_name}** company has been accepted ✅')
            response = self.sheet_manager.insert_company_data(company_name)
            if response:
                await staff_channel.send("Company added to spread sheet successfully! ✅")
            else:
                await staff_channel.send("Company couldn't be added! ❌")
        else:
            await ctx.author.send(f'Sorry, your request to add **{company_name}** company has been declined ❌')
            

async def setup(bot: Bot) -> None:
    """Set up"""
    await bot.add_cog(Company(bot))