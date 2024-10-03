from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import app_commands
import discord
import typing

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

class FormCommand(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @app_commands.command()
    @has_permissions(administrator=True)
    async def form(self):
        #Create a new channel in a forum channel, store the channel ID of the channel
        #Send message with the view, channel ID in the message
            #The view will send a message in the appropriate thread
                #Prompt the user with a modal form, send the message in the thread

        pass