import os

from discord.ext import commands
import discord
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta
from gameParty import gameParty
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = 'gaming ')
parties = []

@bot.command(name='create', help = 'User can join a game party', pass_context = True)
async def create(ctx, game, start: int, duration: int, maxUsers):
    schedule = datetime.today()
    dur = timedelta(seconds=60 * duration)
    party = gameParty(game, schedule.replace(hour= start // 100, minute= start % 100), dur, maxUsers, ctx.message.author)
    parties.append(party)
    embed = discord.Embed(description = 'Succesfully created a game party.')
    member = ctx.message.author
    avatar = member.avatar_url
    embed.set_thumbnail(url = avatar)
    embed.add_field (name = 'Owner', value = party.owner.name)
    embed.add_field(name = 'Game', value = party.game)
    embed.add_field (name = 'Schedule', value = party.startTime.strftime("%H:%M") + '~' + party.endTime.strftime("%H:%M"))
    embed.add_field (name = 'Maximum Participants', value = party.maxUsers, inline = False)
    embed.add_field (name = 'Party ID', value = party.id)
    await ctx.send(embed = embed)
    

@bot.command(name='view', help = 'Displays all existing game parties.', pass_context = True) 
async def view(ctx, game = None):
    if game is not None :
        sortedGameParties = sorted(parties, key = gameParty.getStartTime)
        embed = discord.Embed(Title = 'Game Parties', description = 'Ongoing game Parties')
        for party in sortedGameParties:
            if party.game == game :
                embed.add_field(name = 'Party ' + str(party.id), value = party.game + '\t' + 
                party.startTime.strftime("%H:%M") + '~' + party.endTime.strftime("%H:%M") +'\n' +
                str(len(party.users)) + '\/' + str(party.maxUsers), inline = False)
        await ctx.send(embed = embed)
    
    await ctx.send(embed = embed)        
    sortedGameParties = sorted(parties, key = gameParty.getStartTime)
    embed = discord.Embed(Title = 'Game Parties', description = 'Ongoing game Parties')
    for party in sortedGameParties:
        embed.add_field(name = 'Party ' + str(party.id), value = party.game + '\t' + 
        party.startTime.strftime("%H:%M") + '~' + party.endTime.strftime("%H:%M") +'\n' +
        str(len(party.users)) + '\/' + str(party.maxUsers), inline = False)
    
    await ctx.send(embed = embed)

@bot.command(name='join', help = 'User can join the game party.', pass_context = True)
async def join(ctx, partyID : int):
    result = parties[partyID].partyJoin(ctx.message.author)
    if result == -1 :
        parties[partyID].spareUsers.append(ctx.message.author)
        embed = discord.Embed(description = 'Error!')
        embed.add_field(name = 'Reason', value = 'The party is currently full. You are joined as a backup!')
        await ctx.send(embed = embed)
        member = ctx.message.author
        avatar = member.avatar_url
        embed.set_thumbnail(url = avatar)
        listOfUsers = ''
        for users in parties[partyID].users :
            listOfUsers = listOfUsers + users.name + '\n'
        embed.add_field(name= 'Participants', value = listOfUsers)
        embed.add_field(name= 'Maximum Participants', value = parties[partyID].maxUsers)
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
        await ctx.send(embed = embed)


    
@bot.command(name='leave', help = 'User can leave the game party', pass_context = True)
async def leave(ctx, partyID : int):
    result = parties[partyID].partyLeave(ctx.message.author)
    if result == -1 :
        embed = discord.Embed(description = 'Error!')
        embed.add_field(name = 'Reason', value = 'You are not in the party')
        await ctx.send(embed = embed)
    
    elif result == 0 :
        embed = discord.Embed(description = 'Succesfully left the party.')
        member = ctx.message.author
        avatar = member.avatar_url
        embed.set_thumbnail(url = avatar)
        await ctx.send(embed = embed)
    
    if len(parties[partyID].users) == 0 :
        parties.remove(parties[partyID])
        return 0

@bot.command(name='info', help = 'Displays party information.')
async def info(ctx, partyID : int):
    try:
        parties[partyID]
    except IndexError:
        embed = discord.Embed(description = 'Error!')
        embed.add_field(name = 'Reason', value = 'Party with corresponding ID does not exist.')
        await ctx.send(embed = embed)
        
    embed = discord.Embed(description = parties[partyID].owner.name + '\'s game party.')
    listOfUsers = ''
    for users in parties[partyID].users :
        listOfUsers = listOfUsers + users.name + '\n'
    embed.add_field(name = 'Members', value = listOfUsers)
    embed.add_field(name = 'Schedule', value = 'from ' + parties[partyID].startTime.strftime("%H:%M") + 'to ' + parties[partyID].endTime.strftime("%H:%M"))
    embed.set_thumbnail(url = parties[partyID].owner.avatar_url)
    await ctx.send(embed = embed)
'''
def update():
    nexttime = time.time()
    while True:
        #Get rid of finished game parties
        #Mention users of game party befre 10 min, and start.
        '''
bot.run(TOKEN)
