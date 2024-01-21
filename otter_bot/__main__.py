import asyncio
import os


from discord.ext.commands import Bot
from dotenv import load_dotenv

from otter_bot.common.constants import COMMAND_PREFIX
from otter_bot.startup.intents import get_registered_intents
from otter_bot.startup.cogs import register_cogs

load_dotenv()

async def main() -> None:
    """Principal function"""

    bot: Bot = Bot(
        command_prefix=COMMAND_PREFIX,
        intents=get_registered_intents(),
    )

    async with bot:
        await register_cogs(bot)
        await bot.start(os.environ["DISCORD_TOKEN"])
        


if __name__ == "__main__":
    asyncio.run(main())