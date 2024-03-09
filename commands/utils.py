import nextcord
import psutil
import cpuinfo
import loggerthyst as log
from utils.shared_data import SharedData
from nextcord.ext import commands


# UTILS CLASS
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="List all available slash commands")
    async def help(self, interaction: nextcord.Interaction):
        commands_list = []
        for command in nextcord.Client.get_all_application_commands(self.bot):
            if isinstance(command, nextcord.SlashApplicationCommand):
                commands_list.append(f"{command.get_mention()}: {command.description}")

        commands_string = "\n".join(commands_list)
        embed = nextcord.Embed(title="Help Menu", color=0x06E5C3)
        embed.add_field(name="Commands", value=commands_string, inline=False)
        embed.add_field(
            name="Info",
            value="""Hosted on an OVH VPS, written in Python using the Nextcord wrapper\n
            [Github](<https://github.com/Bluemethyst/WhoAreDis>)\n
            [Support Server](<https://discord.gg/Sc6Es7QnhH>)\n
            [Website](<https://bluemethyst.dev/>)""",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)
        log.info(command="List Commands", interaction=interaction)

    # PING
    @nextcord.slash_command(
        description="Get the latency from the bot to Discords servers"
    )
    async def ping(self, interaction: nextcord.Interaction):
        latency = round(self.bot.latency * 1000, 0)
        embed = nextcord.Embed(title=f"Latency: {latency}MS", color=0x06E5C3)
        await interaction.response.send_message(embed=embed)
        log.info(command="Ping", interaction=interaction)

    @nextcord.slash_command(description="Get information about the bot")
    async def info(self, interaction: nextcord.Interaction):

        cpu_info = cpuinfo.get_cpu_info()
        cpu_name = cpu_info["brand_raw"]
        python_version = cpu_info["python_version"]
        architecture = cpu_info["arch"]

        memory = psutil.virtual_memory()
        memory_used_gb = memory.used / (1024**3)
        memory_total_gb = memory.total / (1024**3)
        memory_percentage = memory.percent
        cpu = psutil.cpu_percent()

        shared_data = SharedData()
        bot_start_time = shared_data.get_bot_start_time()
        unix_timestamp = int(bot_start_time.timestamp())

        embed = nextcord.Embed(title="Info", color=0x06E5C3)
        embed.add_field(
            name=f"Bot ({round(self.bot.latency * 1000, 0)}MS)",
            value="Written in Python using the Nextcord wrapper and hosted on an OVH VPS\n[Source](<https://github.com/Bluemethyst/WhoAreDis>)",
        )
        embed.add_field(name="CPU", value=f"{cpu_name}\n{cpu.real}% in use")
        embed.add_field(name="Architecture", value=architecture)
        embed.add_field(
            name="Memory",
            value=f"{memory_used_gb:.2f}GB/{memory_total_gb:.2f}GB\n{memory_percentage}% in use",
        )
        embed.add_field(name="Python", value=python_version)
        embed.add_field(name="Startup Time", value=f"<t:{unix_timestamp}:R>")

        await interaction.response.send_message(embed=embed)
        log.info(command="Info", interaction=interaction)
