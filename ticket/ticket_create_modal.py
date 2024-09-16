import discord
import typing
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..bot import Bot

import discord.ui as ui  #for UI elements

from helpers.bothelpers import BotHelpers #My own helpers
import json #Needed to access the config
import datetime #Needed for the embed creation

class CreateTicketModal(ui.Modal, title='Create Ticket'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.type = type

    mcusername = ui.TextInput(label="Minecraft Username",style=discord.TextStyle.short,required=True,max_length=20,placeholder="Include . for bedrock!")
    subject = ui.TextInput(label="Subject",style=discord.TextStyle.short,required=True,max_length=20,placeholder="Rampaging Zombies!")
    description = ui.TextInput(label="Description",style=discord.TextStyle.paragraph,required=True,placeholder="Try to be as detailed as you can! Include coordinates for example.")
    
    async def on_submit(self,interaction:discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True,thinking=False)
            #Open the setup JSON
            with open('config.json','r') as file:
                config = json.load(file)
            #Find the current ticket number from the config, increment the counter
            for channel in config["channels"]:
                if config["channels"][f"{channel}"]["id"] == f"{interaction.channel_id}":
                    ticket_id = int(config["channels"][f"{channel}"]["count"])
                    config["channels"][f"{channel}"]["count"] = f"{ticket_id + 1}"
            with open('config.json','w') as file:
                json.dump(config,file,indent=4)

            #Creation of the ticket embed
            embed = discord.Embed(title=f"Ticket #{ticket_id}",
                colour=0x00b0f4,
                description=f'**{self.subject}**\n{self.description}\n\n-`{self.mcusername}`',
                timestamp=datetime.datetime.now())
            embed.set_footer(text=f"{interaction.user.display_name}",
                icon_url=f"{interaction.user.display_avatar}")

            #Creation of the thread
            thread:discord.Thread = await interaction.channel.create_thread(name=f"Ticket #{ticket_id}",invitable=False)

            #Load ticket json
            with open('tickets.json','r') as ticketfile:
                ticketlog = json.load(ticketfile)
            #Log new ticket
            timestamp = datetime.datetime.now()
            epoch = round(timestamp.timestamp())
            new_ticket_info = {
                        "thread_id": f"{thread.id}",
                        "user_id": f"{interaction.user.id}",
                        "status": "New",
                        "mcuser": f"{self.mcusername}",
                        "subj": f"{self.subject}",
                        "desc": f"{self.description}",
                        "epoch": f"{epoch}"
                        }
            ticketlog[f"{ticket_id}"] = new_ticket_info
            #Write to tickets json
            with open('tickets.json','w') as ticketfile:
                json.dump(ticketlog,ticketfile,indent=4)

            #Attach info & invite user to the thread
            from ticket import ticket_close_view
            control_view = ticket_close_view.TicketCloseView(self.bot)
            await thread.send(embed=embed,view=control_view)
            await thread.add_user(interaction.user)

            helloembed = discord.Embed(title="",
                description="Thank you for reaching out to the support team! The support team has been notified, and will be with you soon.")
            await thread.send(embed=helloembed,delete_after=300)

        except Exception as e:
            print(e)