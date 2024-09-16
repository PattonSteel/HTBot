import discord
import typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

import discord.ui as ui  #for UI elements
import json

class ControlButtonView(ui.View):
    def __init__(self, bot: "Bot"):
        super().__init__(timeout=None)
        self.bot = bot
	
    @ui.button(label="Refresh",style=discord.ButtonStyle.primary,custom_id="refreshcontrols")
    async def refresh_controls_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        try:            
            await interaction.channel.typing()

            from control import control
            embed = await control.refresh_control_embed(self.bot,interaction.channel_id)

            done_embed = discord.Embed(
                description="Manually refreshed panel!")
            await interaction.response.send_message(embed=done_embed,delete_after=3,silent=True,ephemeral=True)

        except Exception as e:
            print(str(e))

    @ui.button(label="History",style=discord.ButtonStyle.gray,custom_id="tickethistory")
    async def history_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        try:
            await interaction.channel.typing()

            ticket_history = ""
            ##Pull history from json
            with open('tickets.json','r') as ticketfile:
                ticketlog = json.load(ticketfile)
            
            for ticketitem in ticketlog:
                if ticketlog[ticketitem]["status"] == "Closed":
                    ticket_number = ticketitem
                    ticket_thread_id = ticketlog[ticketitem]["thread_id"]
                    ticket_subj = ticketlog[ticketitem]["subj"]
                    ticket_status = ticketlog[ticketitem]["status"]
                    ticket_user = ticketlog[ticketitem]["user_id"]

                    epoch = ticketlog[ticketitem]["epoch"]
                    ticket_history += f"<t:{epoch}:d> | {ticket_status} | [#{ticket_number}](https://discord.com/channels/{438194489958465538}/{ticket_thread_id}) {ticket_subj} -<@{ticket_user}>\n"

            #Return the content
            history_embed = discord.Embed(
                title="HT Ticket History",
                description=ticket_history
                )
            await interaction.response.send_message(embed=history_embed,delete_after=10,ephemeral=True)

        except Exception as e:
            print(str(e))