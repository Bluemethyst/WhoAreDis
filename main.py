import datetime
import os

import dotenv
import nextcord
from nextcord.ext import commands

from commands.application import ApplicationCmds
from commands.guild import GuildCmds
from commands.user import UserCmds
from commands.utils import Utils
from loggerthyst import info
from utils.shared_data import SharedData

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)
bot.add_cog(Utils(bot))
bot.add_cog(ApplicationCmds(bot))
bot.add_cog(GuildCmds(bot))
bot.add_cog(UserCmds(bot))


@bot.event
async def on_ready():
    info(f"Logged in as {bot.user}")
    await bot.change_presence(
        activity=nextcord.Activity(
            name="with a template!", type=nextcord.ActivityType.playing
        )
    )
    shared_data = SharedData()
    shared_data.set_bot_start_time(datetime.datetime.now())


bot.run(TOKEN)
