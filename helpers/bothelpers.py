import discord
import typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

class BotHelpers():
    def __init__(self, bot: "Bot"):
        self.bot = bot

    #Parses through messages in the channel where the interaction occured, and deletes them
    async def purge_bumpers(self, interaction: discord.Interaction):
        async for message in interaction.channel.history(limit=25):
            if message.flags.silent == True:
                if message.author.id == 1222379698873434232:
                    await message.delete()

    #Parses through messages in the channel where the interaction occured, and deletes them
    async def purge_bumpers_ch(self, channel: discord.TextChannel):
        async for message in channel.history(limit=25):
            if message.flags.silent == True:
                if message.author.id == 1222379698873434232:
                    await message.delete()