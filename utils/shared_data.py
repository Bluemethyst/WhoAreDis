# shared_data.py
import datetime

API = "https://discordlookup.mesavirep.xyz/v1/"

badge_to_emoji = {
    "HOUSE_BRAVERY": "<:discordbravery:1215777627709902969>",
    "HOUSE_BRILLIANCE": "<:discordbrillance:1215777630054518955>",
    "HOUSE_BALANCE": "<:discordbalance:1215777643740401674> ",
    "ACTIVE_DEVELOPER": "<:activedeveloper:1215782358494609419>",
    "DISCORD_EMPLOYEE": "<:discordemployee:1215777659007668317>",
    "EARLY_VERIFIED_BOT_DEVELOPER": "<:verifiedbotdev:1215782096283635834>",
    "EARLY_SUPPORTER": "<:discordearlysupporter:1215777634990952468>",
    "NITRO": "<:discordnitro:1215777631996477572>",
    "HYPESQUAD_EVENTS": "<:discordhypesquad:1215777637163602020>",
    "PARTNERED_SERVER_OWNER": "<:discordpartner:1215777645913051299>",
    "BUGHUNTER_LEVEL_1": "<:discordbughunterlv1:1215777648454926358>",
    "BUGHUNTER_LEVEL_2": "<:discordbughunterlv2:1215777652057833472>",
}


class SharedData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.bot_start_time = None
        return cls._instance

    def set_bot_start_time(self, start_time):
        self.bot_start_time = start_time

    def get_bot_start_time(self):
        return self.bot_start_time
