# bot.py
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = 'gaming')



@bot.command(name='join', help = 'User can join a game party')
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)