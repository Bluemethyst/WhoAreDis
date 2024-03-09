import httpx
import nextcord
import loggerthyst as log
from datetime import datetime
from utils.funcs import get_most_common_color
from utils.shared_data import API
from nextcord.ext import commands


class ApplicationCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Fetch information about an application")
    async def application(
        self,
        interaction: nextcord.Interaction,
        app: nextcord.User = nextcord.SlashOption(
            name="app_id",
            description="The application to fetch information about",
            required=True,
        ),
    ):
        await interaction.response.defer()
        app_r = httpx.get(API + "application/" + str(app.id))
        user_r = httpx.get(API + "user/" + str(app.id), timeout=10)
        data_app = app_r.json()
        data_user = user_r.json()
        date_string = data_user["created_at"]
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        epoch_timestamp = date_object.timestamp()
        desc_str = ""
        intents_str = ""
        if (
            "message" not in data_app
            and data_app.get("message") != "Unknown application"
        ):
            if data_user["id"]:
                desc_str += f"**ID:** {data_user['id']}\n"
            if data_user["username"]:
                desc_str += f"**Username:** {data_user['username']} <:bottag:1215777655811739729>\n"
            if data_user["created_at"]:
                desc_str += f"**Created on:** <t:{int(epoch_timestamp)}>\n"
            if data_app["description"]:
                desc_str += f"**Description:** {data_app['description']}\n"
            if data_app["summary"]:
                desc_str += f"**Summary:** {data_app['summary']}\n"
            if data_app["type"]:
                desc_str += f"**Type:** {data_app['type']}\n"
            desc_str += f"**Is Monetized?** {data_app['is_monetized']}\n"
            desc_str += f"**Hook?** {data_app['hook']}\n"
            desc_str += f"**Bot Public?** {data_app['bot_public']}\n"
            desc_str += (
                f"**Bot Requires Code Grant?** {data_app['bot_require_code_grant']}\n"
            )
            if data_app["flags"]["detailed"]:
                for intent in data_app["flags"]["detailed"]:
                    formatted_badge = " ".join(
                        word.capitalize() for word in intent.split("_")
                    )
                    intents_str += formatted_badge + ", "
                desc_str += f"**Flags:** {intents_str.rstrip(', ')}\n"
            embed = nextcord.Embed(
                color=nextcord.Color.from_rgb(
                    *get_most_common_color(data_user["avatar"]["link"])
                ),
                title=f"Information on {data_user['username']}",
                description=desc_str,
            )
            embed.set_thumbnail(url=data_user["avatar"]["link"])
            await interaction.followup.send(embed=embed)
        else:
            embed = nextcord.Embed(
                color=0x06E5C3,
                title=f"ERROR",
                description="Application not found. Please make sure you entered the correct ID and the application is not a user.",
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        log.info(command="Application", interaction=interaction)
