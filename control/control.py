import discord
import typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

from helpers.bothelpers import BotHelpers #My own helpers
import json #Needed to access the config
import datetime #Needed for the embed

#Generate a control panel by parsing through the different channels in the config JSON, then collecting the messages here.
async def control_embed(self):
    embed = discord.Embed(title="HT Control Panel",
        colour=0xffffff,
        timestamp=datetime.datetime.now())
    embed.set_footer(text="Last refreshed")

    with open('config.json','r') as file:
        config = json.load(file)

    #Generate fields to view all suggestions
    for channel in config['channels']:
        ch_type = config["channels"][f"{channel}"]["type"]
        ch_id = config["channels"][f"{channel}"]["id"]
        guild_id = config["guild_id"]

        ch_content = ""
        match f"{ch_type}":
            case "suggestion":
                ch_object: discord.TextChannel = await self.fetch_channel(ch_id)
                async for message in ch_object.history(limit=100):
                    #If the message has an embed
                    if message.embeds != []:
                        #Obtain the suggestion ID
                        suggestion_num = message.embeds[0].title      
                        #Convert time of the message to a unix timestamp for Discord syntax
                        if message.edited_at == None:
                            timestamp = message.created_at
                        else:
                            timestamp = message.edited_at
                        epoch = round(timestamp.timestamp())
                        #Make a preview of the suggestion 
                        suggestion_preview = message.embeds[0].description
                        suggestion_preview = suggestion_preview.split('\n')[0]
                        suggestion_preview = suggestion_preview.replace('*','')

                        ch_content += f"<t:{epoch}:d> | [{suggestion_num[11:]}](https://discord.com/channels/{guild_id}/{ch_id}/{message.id}) {suggestion_preview[:20]}\n"
                embed.add_field(name=f"{channel}", value=ch_content, inline=False)

            case "support":
                with open('tickets.json','r') as ticketfile:
                    ticketlog = json.load(ticketfile)
                
                for ticketitem in ticketlog:
                    if ticketlog[ticketitem]["status"] != "Closed":
                        ticket_number = ticketitem
                        ticket_thread_id = ticketlog[ticketitem]["thread_id"]
                        ticket_subj = ticketlog[ticketitem]["subj"]
                        ticket_status = ticketlog[ticketitem]["status"]
                        ticket_user = ticketlog[ticketitem]["user_id"]

                        epoch = ticketlog[ticketitem]["epoch"]
                        ch_content += f"<t:{epoch}:d> | {ticket_status} | [#{ticket_number}](https://discord.com/channels/{guild_id}/{ticket_thread_id}) {ticket_subj} -<@{ticket_user}>\n"
                    
                embed.add_field(name=f"{channel}",value=ch_content)

    return embed

async def refresh_control_embed(self,ch_id, **kwargs):
    no_resent = kwargs.get('no_resent',False)

    control_channel: discord.TextChannel = await self.fetch_channel(ch_id)
    async for message in control_channel.history(limit=1):
        old_tickets = message.embeds[0].fields[-1]
        old_message = message

    new_panel:discord.Embed = await control_embed(self)
    if ((new_panel.fields[-1].value[:-1] == old_tickets.value) or no_resent):
        await old_message.edit(embed=new_panel)

    else:
        await message.delete()
        from control import control_bumper_view
        view = control_bumper_view.ControlButtonView(self)
        await control_channel.send(embed=new_panel,view=view,silent=True)
