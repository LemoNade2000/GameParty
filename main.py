import os

from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta
from gameParty import gameParty

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = 'gaming')

@bot.command(name='join', help = 'User can join a game party', pass_context = True)
async def join(ctx):
    dur = timedelta(seconds=3600)
    newParty = gameParty(datetime.now(), dur, 5, ctx.message.author)
    await ctx.send("User joined the party.")
    newParty.partyInfo()

bot.run(TOKEN)