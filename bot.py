from discord.ext import commands, tasks
import discord

#/import cogs here
from helpers.setup import SetupCommand
from suggestion.suggestion import SuggestionCommand

#/import views here
from suggestion.suggestion_bumper_view import SuggestionButtonView
from control.control_bumper_view import ControlButtonView
from ticket.ticket_bumper_view import TicketButtonView
from ticket.ticket_close_view import TicketCloseView

class Bot(commands.Bot):
    def __init__(self, **options):
        intents = discord.Intents.default()
        intents.message_content = True  
        super().__init__(intents=intents, command_prefix='/')
    
    async def setup_hook(self):
        #/add views here
        self.add_view(SuggestionButtonView(self))
        self.add_view(ControlButtonView(self))
        self.add_view(TicketButtonView(self))
        self.add_view(TicketCloseView(self))

    async def on_ready(self):
        print(f'Logged in as {self.user}!')
        #/add commands here
        await self.add_cog(SetupCommand(self))
        await self.add_cog(SuggestionCommand(self))

        self.refresh.start()

        synced = await self.tree.sync()
        print("{} commands synced".format(len(synced)))

    async def on_message(self, message:discord.Message):
        #SHOULD REDO THIS LOL
        if message.channel.id == 1222388800513380393:   #staff-log
            if message.author.id == 1241832221082521740:   #webhook-user
                await message.create_thread(name="Notes")

        if message.channel.id == 1209563764207128576:   #applications
            if message.author.id == 1209964403357777921:   #webhook-user
                applicant_username = message.content.split(' ')[0]
                await message.create_thread(name=f"{applicant_username}")
                await message.add_reaction('⬆️')
                await message.add_reaction('⬇️')
        
    @tasks.loop(minutes=5)
    async def refresh(self):
            from control import control
            embed = await control.refresh_control_embed(self,1274560583751962634)