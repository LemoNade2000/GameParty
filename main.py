import os

from discord.ext import commands
import discord
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta
from gameParty import gameParty

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = 'gaming ')
parties = []

@bot.command(name='create', help = 'User can join a game party', pass_context = True)
async def create(ctx, start: int, duration: int, maxUsers):
    schedule = datetime.today()
    dur = timedelta(seconds=60 * duration)
    party = gameParty(schedule.replace(hour= start // 100, minute= start % 100), dur, maxUsers, ctx.message.author, len(parties))
    parties.append(party)
    embed = discord.Embed(description = 'Succesfully created a game party.')
    member = ctx.message.author
    avatar = member.avatar_url
    embed.set_thumbnail(url = avatar)
    embed.add_field (name = 'Owner', value = party.owner.name)
    embed.add_field (name = 'Schedule', value = party.startTime.strftime("%H:%M") + '~' + party.endTime.strftime("%H:%M"))
    embed.add_field (name = 'Maximum Participants', value = party.maxUsers, inline = False)
    embed.add_field (name = 'Party ID', value = party.id)
    await ctx.send(embed = embed)
    

@bot.command(name='view', help = 'User can see how many parties there are.', pass_context = True) 
async def view(ctx):
    sortedGameParties = sorted(parties, key = gameParty.getStartTime)
    embed = discord.Embed(Title = 'Game Parties', description = 'Ongoing game Parties')
    for party in sortedGameParties :
        embed.add_field(name ='from ' + party.startTime.strftime("%H:%M") + 'to ' + party.endTime.strftime("%H:%M"), value = party.owner.name + '\t' + '(' + str(len(party.users)) + '/' + str(party.maxUsers) + ')', inline = False)
    await ctx.send(embed = embed)


@bot.command(name='join', help = 'User can join the game party.', pass_context = True)
async def join(ctx, partyID : int):
    result = parties[partyID].partyJoin(ctx.message.author)
    if result == -1 :
        embed = discord.Embed(description = 'Error!')
        embed.add_field(name = 'Reason', value = 'The party is currently full.')
        await ctx.send(embed = embed)

    elif result == -2 :
        embed = discord.Embed(description = 'Error!')
        embed.add_field(name = 'Reason', value = 'You are already in the party.')
        await ctx.send(embed = embed) 

    elif result == 0 :
        embed = discord.Embed(description = 'Succesfully joined the party.')
        member = ctx.message.author
        avatar = member.avatar_url
        embed.set_thumbnail(url = avatar)
        listOfUsers = ''
        for users in parties[partyID].users :
            listOfUsers = listOfUsers + users.name + '\n'
        embed.add_field(name= 'Participants', value = listOfUsers)
        embed.add_field(name= 'Maximum Participants', value = parties[partyID].maxUsers)
        ctx.send(embed = embed)


    
#@bot.command(name='leave', help = 'User can leave the game party', pass_context = True)
#async def leave(ctx, partyID : int):

bot.run(TOKEN)
