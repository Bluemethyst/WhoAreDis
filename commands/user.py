import httpx
import nextcord
import loggerthyst as log
from datetime import datetime
from utils.shared_data import API, badge_to_emoji
from nextcord.ext import commands


class UserCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Fetch information about a user")
    async def user(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.User = nextcord.SlashOption(
            name="user_id",
            description="The user to fetch information about, you, if left blank",
            required=False,
        ),
    ):
        await interaction.response.defer()
        if user:
            r = httpx.get(API + "user/" + str(user.id))
        else:
            r = httpx.get(API + "user/" + str(interaction.user.id))
        data = r.json()
        date_string = data["created_at"]
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        epoch_timestamp = date_object.timestamp()
        desc_str = ""
        badge_str = ""
        if data["id"]:
            desc_str += f"**ID:** {data['id']}\n"
        if data["username"]:
            desc_str += f"**Username:** {data['username']}\n"
        if data["created_at"]:
            desc_str += f"**Created on:** <t:{int(epoch_timestamp)}>\n"
        desc_str += f"**Animated Avatar?** {data['avatar']['is_animated']}\n"
        if data["badges"]:
            emojis = [badge_to_emoji.get(badge, badge) for badge in data["badges"]]
            for emoji in emojis:
                badge_str += emoji + " "
            desc_str += f"**Badges:** {badge_str}\n"
        if data["premium_type"]:
            desc_str += f"**Premium Type:** {data['premium_type']}\n"
        embed = nextcord.Embed(
            color=data["accent_color"],
            title=f"Information on {data['global_name']}",
            description=desc_str,
        )
        if data["banner"]["link"]:
            embed.set_image(url=data["banner"]["link"])
        embed.set_thumbnail(url=data["avatar"]["link"])
        await interaction.followup.send(embed=embed)
        log.info(command="User", interaction=interaction)
