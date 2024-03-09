import httpx
import nextcord
from nextcord.ext import commands

import loggerthyst as log
from utils.funcs import get_most_common_color
from utils.shared_data import API


class GuildCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Fetch information about a guild")
    async def guild(
        self,
        interaction: nextcord.Interaction,
        guild=nextcord.SlashOption(
            name="guild_id",
            description="The guild to fetch information about, the current guild if left blank",
            required=False,
        ),
    ):
        await interaction.response.defer()
        local = False
        image = None
        if guild:
            r = httpx.get(API + "guild/" + str(guild))
            local = False
        else:
            local = True
        if local:
            guild = interaction.guild
            desc_str = ""
            if guild.id:
                desc_str += f"**ID:** {guild.id}\n"
            if guild.name:
                title = guild.name
            if guild.description:
                desc_str += f"**Description:** {guild.description}\n"
            if guild.created_at:
                desc_str += f"**Created at:** <t:{int(guild.created_at.timestamp())}>\n"
            if guild.member_count:
                desc_str += f"**Member Count:** {guild.member_count}\n"
            if guild.premium_tier:
                desc_str += f"**Premium Tier:** {guild.premium_tier}\n"
            if guild.premium_subscription_count:
                desc_str += (
                    f"**Premium Subscriptions:** {guild.premium_subscription_count}\n"
                )
            if guild.emojis:
                desc_str += f"**Emoji Count:** {len(guild.emojis)}\n"
                desc_str += (
                    f"**Emojis:** {' '.join([str(emoji) for emoji in guild.emojis])}\n"
                )
            if guild.stickers:
                desc_str += f"**Sticker Count:** {len(guild.stickers)}\n"
                desc_str += f"**Stickers:** {', '.join([str(sticker) for sticker in guild.stickers])}\n"
            if guild.icon:
                image = guild.icon.url

        else:
            data = r.json()
            desc_str = ""
            ephermeral = False
            if r.status_code == 200 and "error" in data and data["error"] is None:
                desc_str += (
                    "### Bot not in specified guild, falling back to public data.\n"
                )
                if data["id"]:
                    desc_str += f"**ID:** {data['id']}\n"
                if data["name"]:
                    desc_str += f"**Name:** {data['name']}\n"
                if data["instant_invite"]:
                    desc_str += f"**Invite:** {data['instant_invite']}\n"
                if data["presence_count"]:
                    desc_str += f"**Online Users:** {data['presence_count']}\n"
            if desc_str == "":
                desc_str = "No information available; the guild is either non-existant, unavailable, or has Server Widget/Discovery disabled."
                title = "ERROR"
                ephermeral = True
            else:
                title = f"Information on {data['name']}"
        embed = nextcord.Embed(
            color=0x06E5C3,
            title=title,
            description=desc_str,
        )
        if image:
            embed.set_thumbnail(url=image)
            embed.color = nextcord.Color.from_rgb(*get_most_common_color(image))
        await interaction.followup.send(embed=embed, ephemeral=ephermeral)
        log.info(command="Guild", interaction=interaction)
