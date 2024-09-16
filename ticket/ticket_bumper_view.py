import discord
import typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

import discord.ui as ui  #for UI elements

class TicketButtonView(ui.View):
    def __init__(self, bot: "Bot"):
        super().__init__(timeout=None)
        self.bot = bot
	
    @ui.button(label="Contact Support",style=discord.ButtonStyle.primary,custom_id="contactsupport")
    async def support_contact_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        try:            
            from ticket.ticket_create_modal import CreateTicketModal
            await interaction.response.send_modal(CreateTicketModal(self.bot))
            
        except Exception as e:
            print(str(e))
            await interaction.response.send_message(content='Error! Please check the console for more information.' ,ephemeral=True)


    @ui.button(label="Appeal Ban",style=discord.ButtonStyle.secondary,custom_id="appealban")
    async def appeal_ban_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        try:            
            from ticket.ticket_create_modal import CreateTicketModal
            await interaction.response.send_modal(CreateTicketModal(self.bot))
            
        except Exception as e:
            print(str(e))
            await interaction.response.send_message(content='Error! Please check the console for more information.' ,ephemeral=True)

    @ui.button(label="Report User",style=discord.ButtonStyle.danger,custom_id="reportuser")
    async def report_user_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        try:            
            from ticket.ticket_create_modal import CreateTicketModal
            await interaction.response.send_modal(CreateTicketModal(self.bot))
            
        except Exception as e:
            print(str(e))
            await interaction.response.send_message(content='Error! Please check the console for more information.' ,ephemeral=True)