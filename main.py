#--------------------------imports---------------------------
import os
import discord
#--------------------------imports---------------------------

#--------------------------Froms--------------------------
from discord.ext import commands
#--------------------------Froms--------------------------
#--------------------------?--------------------------

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='!',
help_command=None, 
case_insensitive = True, 
intents = intents)
#--------------------------?--------------------------
#--------------------------Events--------------------------

@client.event
async def on_ready():
    print(f'EU entrei como {client.user}')

@client.event
async def on_message(message):

    await client.process_commands(message)

    if message.author == client.user: return

    if message.author.bot: return
    
    if message.mention_everyone: return

#--------------------------Events--------------------------

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')

client.run('token') #Token do bot aqui