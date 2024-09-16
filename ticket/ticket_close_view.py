import discord
import typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

import discord.ui as ui  #for UI elements
import json #Needed to access the ticket log

class TicketCloseView(ui.View):
    def __init__(self, bot: "Bot"):
        super().__init__(timeout=None)
        self.bot = bot
	
    @ui.button(label="Close Ticket",style=discord.ButtonStyle.primary,custom_id="closeticket")
    async def close_ticket_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        try:    
            await interaction.response.defer(thinking=False)
            await interaction.channel.typing()        
            #Load ticket json
            with open('tickets.json','r') as ticketfile:
                ticketlog = json.load(ticketfile)
            #change status in the JSON
            for ticket in ticketlog:
                threadid = ticketlog[ticket]["thread_id"]
                if int(threadid) == interaction.channel.id:
                    ticketlog[f"{ticket}"]["status"] = "Closed"
            #write to ticket
            with open('tickets.json','w') as ticketfile:
                json.dump(ticketlog,ticketfile,indent=4)
            
            #close and lock the thread
            byembed = discord.Embed(title="",
                description=f"This ticket has been closed by <@{interaction.user.id}>")
            await interaction.channel.send(embed=byembed)
            await interaction.channel.edit(locked=True)

            #Should also refresh the control panel, by editing and not sending a new message.
            from control import control
            embed = await control.refresh_control_embed(self.bot,1274560583751962634,no_resent=True)
            
        except Exception as e:
            print(str(e))