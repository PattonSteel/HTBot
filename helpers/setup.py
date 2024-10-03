import discord
import typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

from discord import app_commands    #for cogs
from discord.ext import commands    #for cogs
from discord.ext.commands import has_permissions #to restrict cmd usage to a permission

from helpers.bothelpers import BotHelpers #My own helpers
import json #Needed to access the config

class SetupCommand(commands.Cog):
    def __init__(self, bot: "Bot"):
        self.bot = bot

    @app_commands.command()
    @has_permissions(administrator=True)
    @app_commands.describe(option='Designate channel for')
    async def setup(self,  interaction: discord.Interaction, option: typing.Literal['suggestion','control','support']):
        #try:
            await interaction.response.defer(thinking=False)
            await interaction.channel.typing()

            channel_type = BotHelpers.channel_lookup(interaction.channel_id)

            #Check to see if the channel is already set up
            if channel_type != None:
                await interaction.channel.send(
                    content=f"This channel is already designated as a {channel_type} channel.",
                    delete_after=5)  
            else:
                #Creates a new entry based off options selected
                BotHelpers.channel_add(channel_id=interaction.channel_id,channel_name=interaction.channel.name,option=option)

            #Run the bumper for the channel depending on the type
            match f"{option}":
                case "suggestion":
                    #Resends the bumper, deletes other silent messages
                    await BotHelpers.purge_bumpers(self,interaction)
                    from suggestion import suggestion_bumper_view
                    suggestion_view = suggestion_bumper_view.SuggestionButtonView(self.bot)
                    suggestion_message = await interaction.channel.send(view=suggestion_view, silent=True) 

                case "support":
                    #Resends the bumper, deletes other silent messages
                    await BotHelpers.purge_bumpers(self,interaction)
                    from ticket import ticket_bumper_view
                    ticket_view = ticket_bumper_view.TicketButtonView(self.bot)
                    support_embed = discord.Embed(title="Hollowtree Tickets",
                        description="",
                        colour=0x05ef69)
                    support_embed.add_field(name="General Support",
                        value="If you need general support please click the `Contact Support` button,",
                        inline=False)
                    support_embed.add_field(name="Punishment Appeals",
                        value="If you believe you've been wrongfully punished, please click the `Appeal Ban` button,",
                        inline=False)
                    support_embed.add_field(name="Player / Staff Report",
                        value="In order to report a player or staff, select the `Report User` button below.",
                        inline=False)

                    ticket_message = await interaction.channel.send(view=ticket_view,embed=support_embed,silent=True)
                
                case "control":
                    #Resends the bumper, deletes other silent messages
                    await BotHelpers.purge_bumpers(self,interaction)
                    from control import control
                    control_embed = await control.control_embed(self.bot)
                    from control import control_bumper_view
                    control_view = control_bumper_view.ControlButtonView(self.bot)
                    
                    control_message = await interaction.channel.send(embed=control_embed, view=control_view,silent=True)

            #Deletes the thinking defer symbol
            await interaction.delete_original_response()

        #except Exception as e:
        #    print(str(e))