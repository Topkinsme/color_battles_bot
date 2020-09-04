#a bot by top

import discord
import logging
from discord.utils import get
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Bot
import asyncio
import random
import time
import datetime
from datetime import date
import json
import dhooks
from dhooks import Webhook
import os
import pymongo,dns
import keep_alive


token = str(os.environ.get("tokeno"))
dbpass=str(os.environ.get("dbpass"))

bot = commands.Bot(command_prefix =commands.when_mentioned_or('!','$'))


#bot.remove_command('help')

client = pymongo.MongoClient("mongodb+srv://Topkinsme:"+dbpass+"@top-cluster.x2y8s.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test

'''
Gamestates:-
0.None
1.Signups open
2.Signups closed
3.Game
4.Game done
'''

#events

@bot.event
async def on_ready():
    print("Working boi!")
    global data
    global annchannel
    global spamchannel
    global gamestate
    global lstmsg
    spamchannel=bot.get_channel(450698253508542474)
    await spamchannel.send("The bot is online!")
    lstmsg={}
    try:
        my_collection = db.main
        data = my_collection.find_one()
        gamestate = data['gamestate']
        '''with open('data.json','r') as f:
            data = json.load(f)
            print(data)
            gamestate = data['gamestate']'''
    except:
            print("Could not load the data")
            data = {}
            data['signedup']={}
            data['gamestate']=0
            gamestate=0
            data['money']={}
            data['roles']=[]
            data['rt']={}
            data['chnls']={}
            data['specters']=[]
            data['code']={}
            data['auction']={}
            data['building']={}
            data['smarket']={}
            dump()
            await spamchannel.send("Warning! Data.json wasn't found. Please check if anything is wrong.")
    if int(gamestate)==1:
        await bot.change_presence(activity=discord.Game(name="Signups open!", type=1))
    elif int(gamestate)==2:
        await bot.change_presence(activity=discord.Game(name="Signups are closed.A game will soon begin.", type=1))
    elif int(gamestate)==3:
        await bot.change_presence(activity=discord.Game(name="Game running.", type=1))
    elif int(gamestate)==4:
        await bot.change_presence(activity=discord.Game(name="Game concluded!", type=1))
    else:
        await bot.change_presence(activity=discord.Game(name=" Colour battles!", type=1))
    my_loop.start()
    my_looptwo.start()
    my_loopthree.start()
    
@tasks.loop(minutes=5)
async def my_loop():
    global earnd
    global lstmsg
    earnd=[]


@tasks.loop(minutes=60)
async def my_looptwo():
    global data
    if int(gamestate)!=3:
      return
    try:
      if data['smarket']['state']==0:
        return
      guildd=bot.get_guild(448888674944548874)
      channel=bot.get_channel(int(data['smarket']['chn']))
      msgid = int(data['smarket']['msg'])
      msg = await channel.fetch_message(msgid)
      await change()
      a=data['smarket']['stocks']['sun']
      b=data['smarket']['stocks']['smirk']
      c=data['smarket']['stocks']['smile']
      d=data['smarket']['stocks']['joy']
      e=data['smarket']['stocks']['pens']
      await msg.edit(content="Cost of :sunglasses: is {} \nCost of :smirk: is {} \nCost of :smiley: is {} \nCost of :joy: is {} \nCost of :pensive: is {} \n".format(a,b,c,d,e))
    except:
      return

@tasks.loop(minutes = 1)
async def my_loopthree():
  datee = datetime.datetime.now()
  if int(datee.strftime("%M"))%10 !=0 :
    return 
  datee = datetime.datetime.now()
  #edit date
  x=bot.get_channel(750580343068688404)
  await x.edit(name="📅 " + datee.strftime("%a") + " " + datee.strftime("%b") + " " + datee.strftime("%d"))
  #edit time
  localtime= datetime.datetime.now()
  x=bot.get_channel(750583960890900542)
  await x.edit(name="🕐 "+ localtime.strftime("%I") + ":" + localtime.strftime("%M") + " "+ localtime.strftime("%p") + " UTC")
  guildd=bot.get_guild(448888674944548874)
  peoples = guildd.members
  a=0
  for person in peoples:
    a+=1
  #edit people
  x=bot.get_channel(750580458957439008)
  if int(gamestate)==1:
        people=0
        for person in data['signedup']:
          people+=1
        await x.edit(name="❗ Signups open! {}/∞".format(people))
  elif int(gamestate)==2:
        await x.edit(name="❎ Signups closed." )
  elif int(gamestate)==3:
        people=0
        total=0
        for member in data['players']:
          total+=1
          if data['players'][member]['state']==1:
            people+=1
        await x.edit(name="🔰 Game in progress. {}/{}".format(people,total)) 
  elif int(gamestate)==4:
        await x.edit(name="✅ Game concluded.")
  else:
        await x.edit(name="⏸️ No game.")
                        
@bot.event
async def on_message(message):
    global gamestate
    if message.author.id == 450320950026567692:
        return
    await bot.process_commands(message)
    if int(gamestate) != 3:
        return
    ath=str(message.author.id)
    fath=message.author
    channel = message.channel
    await score(ath,message.content)
    if message.channel.name!="battlefield":
      return
    n = random.randint(0,500)
    cash = random.randint(100,500)
    if n ==49:
      emoji = "🎁"
      await message.add_reaction(emoji)
      await message.channel.send(":tada: <@{}> has just won a prize of {}".format(ath,cash))
      try:
        data['money'][ath]+=cash
      except:
        await message.channel.send("It seems I had trouble accessing your account so I'm just going to have to keep the money with myself....")
      dump()
    
@bot.event
async def on_command_error(ctx,error):
    await ctx.send(error)

@bot.event
async def on_member_join(member):
    await spamchannel.send("{} joined the server".format(member.mention))
    
@bot.event
async def on_member_remove(member):
    await spamchannel.send("{} left the server".format(member.mention))
    
@bot.event
async def on_message_delete(message):
    await spamchannel.send("'{}' was deleted in <#{}>".format(message.content,message.channel.id))
    
@bot.event
async def on_user_update(before,after):
    if before.name==after.name:
        return
    else:
        await spamchannel.send("'{}' has changed his name to '{}' .".format(before.name,after.name))

@bot.event
async def on_raw_reaction_add(payload):
    if int(gamestate)!=3:
      return
    userid=payload.user_id
    msgid=payload.message_id
    channelid=payload.channel_id
    guildd=bot.get_guild(448888674944548874)
    channel=bot.get_channel(channelid)
    userr=discord.utils.get(guildd.members,id=userid)
    emoji=str(payload.emoji)
    msg = await channel.fetch_message(msgid)
    #print(emoji)
    role1 = discord.utils.get(guildd.roles, name="Alive")
    role2 = discord.utils.get(guildd.roles, name="Respawning")
    role3 = discord.utils.get(guildd.roles, name="Dead")
    role4 = discord.utils.get(guildd.roles, name="Spectator")
    if role2 in userr.roles or role3 in userr.roles or role4 in userr.roles:
      await msg.remove_reaction(emoji,userr)
    elif role1 in userr.roles and emoji=="📌":
      await msg.pin()

@bot.event
async def on_raw_reaction_remove(payload):
    if int(gamestate)!=3:
      return
    userid=payload.user_id
    msgid=payload.message_id
    channelid=payload.channel_id
    guildd=bot.get_guild(448888674944548874)
    channel=bot.get_channel(channelid)
    userr=discord.utils.get(guildd.members,id=userid)
    emoji=str(payload.emoji)
    msg = await channel.fetch_message(msgid)
    #print(emoji)
    role1 = discord.utils.get(guildd.roles, name="Alive")
    role2 = discord.utils.get(guildd.roles, name="Respawning")
    role3 = discord.utils.get(guildd.roles, name="Dead")
    role4 = discord.utils.get(guildd.roles, name="Spectator")
    if role2 in userr.roles or role3 in userr.roles or role4 in userr.roles:
      return
    elif role1 in userr.roles and emoji=="📌":
      await msg.unpin()



#admin/informer

@bot.command()
@commands.has_role("Informer")
async def logout(ctx):
    '''Shuts down the bot <Informer>'''
    await ctx.send("Logging out.")
    await bot.logout()
    dump()
    
@bot.command()
@commands.has_role("Informer")
async def purge(ctx,number=5):
    '''Deletes a ceratin number of messages. <Informer>'''
    chnl=ctx.channel
    await chnl.purge(limit=number+1)
    await ctx.send("Purged {} messages.".format(number))
    
@bot.command()
@commands.has_role("Informer")
async def compreset(ctx):
    '''Complete reset. <Informer>'''
    global data
    global gamestate
    data = {}
    data['signedup']={}
    data['gamestate']=0
    gamestate=0
    await bot.change_presence(activity=discord.Game(name=" Colour battles!", type=1))
    data['money']={}
    data['roles']=[]
    data['rt']={}
    data['chnls']={}
    data['specters']=[]
    data['code']={}
    data['auction']={}
    data['building']={}
    data['smarket']={}
    await ctx.send("A complete erasure of all data has been done.")
    dump()
    
@bot.command()
@commands.has_role("Informer")
async def pdata(ctx):
    '''Send the complete data file. <Informer>'''
    print(data)
    await ctx.send(data)
    
 
    
@bot.command()
@commands.has_role("nuke")
async def nuke(ctx):
    '''Empties the entire channel <Nuke>'''
    chnl=ctx.message.channel
    async for message in chnl.history(limit=10000):
        await message.delete()
    tempc = await ctx.send("Cleared.")
    await asyncio.sleep(30)
    await tempc.delete()
    
@bot.command(aliases=["gs"])
@commands.has_role("Informer")
async def cgamestate(ctx,num):
    '''Manually changes gamestate. <Informer>'''
    global gamestate
    global data
    if (int(num)<0 or int(num)>4):
        await ctx.send("That is wrong. Please check the number again. Gamestate number must be always between 0 and 4.")
        return
    gamestate=num
    data['gamestate']=gamestate
    print(gamestate)
    if int(gamestate)==1:
        await ctx.send("Signups open!")
        await bot.change_presence(activity=discord.Game(name="Signups open!", type=1))
    elif int(gamestate)==2:
        await ctx.send("Signups closed!")
        await bot.change_presence(activity=discord.Game(name="Signups are closed.A game will soon begin.", type=1))
    elif int(gamestate)==3:
        await ctx.send("Game has started!")
        await bot.change_presence(activity=discord.Game(name="Game running.", type=1))
    elif int(gamestate)==4:
        await ctx.send("Game has concluded!")
        await bot.change_presence(activity=discord.Game(name="Game concluded!", type=1))
    else:
        await bot.change_presence(activity=discord.Game(name=" Colour battles!", type=1))
    dump()
    
@bot.command()
@commands.has_role("Informer")
async def reset(ctx):
    '''Resets game .<Informer>'''
    global data
    global gamestate
    for user in data['players']:
        guildd=bot.get_guild(448888674944548874)
        userr=discord.utils.get(guildd.members,id=int(user))
        role = discord.utils.get(guildd.roles, name="Spectator")
        await userr.remove_roles(role)
        role = discord.utils.get(guildd.roles, name="Dead")
        await userr.remove_roles(role)
        role = discord.utils.get(guildd.roles, name="Respawning")
        await userr.remove_roles(role)
        role = discord.utils.get(guildd.roles, name="Alive")
        await userr.remove_roles(role)
        role = discord.utils.get(guildd.roles, name="Players")
        await userr.remove_roles(role)
    for user in data['specters']:
        guildd=bot.get_guild(448888674944548874)
        userr=discord.utils.get(guildd.members,id=int(user))
        role = discord.utils.get(guildd.roles, name="Spectator")
        await userr.remove_roles(role)
    namee= data['code']['gamecode']
    cate = discord.utils.get(ctx.message.guild.categories, name=namee)
    #print(cate.channels)
    for channel in cate.channels:
        await channel.delete()
    await cate.delete()
    namee= str(data['code']['gamecode']) + ' factions'
    cate2 = discord.utils.get(ctx.message.guild.categories, name=namee)
    #print(cate2.channels)
    for channel in cate2.channels:
        await channel.delete()
    await cate2.delete()
    if data['code']['ccno']>0:
      namee=data['code']['gamecode'] + ' cc1'
      cate = discord.utils.get(ctx.message.guild.categories, name=namee)
      #print(cate.channels)
      for channel in cate.channels:
        await channel.delete()
      await cate.delete()
    if data['code']['ccno']>50:
      namee=data['code']['gamecode'] + ' cc2'
      cate = discord.utils.get(ctx.message.guild.categories, name=namee)
      #print(cate.channels)
      for channel in cate.channels:
        await channel.delete()
      await cate.delete()
    if data['code']['ccno']>100:
      namee=data['code']['gamecode'] + ' cc3'
      cate = discord.utils.get(ctx.message.guild.categories, name=namee)
      #print(cate.channels)
      for channel in cate.channels:
        await channel.delete()
      await cate.delete()
    if data['code']['ccno']>150:
      namee=data['code']['gamecode'] + ' cc4'
      cate = discord.utils.get(ctx.message.guild.categories, name=namee)
      #print(cate.channels)
      for channel in cate.channels:
        await channel.delete()
      await cate.delete()
    if data['code']['ccno']>200:
      namee=data['code']['gamecode'] + ' cc5'
      cate = discord.utils.get(ctx.message.guild.categories, name=namee)
      #print(cate.channels)
      for channel in cate.channels:
          await channel.delete()
      await cate.delete()
    data = {}
    data['signedup']={}
    data['gamestate']=0
    gamestate=0
    await bot.change_presence(activity=discord.Game(name=" Colour battles!", type=1))
    data['money']={}
    data['roles']=[]
    data['rt']={}
    data['specters']=[]
    data['players']={}
    data['chnls']={}
    data['code']={}
    data['auction']={}
    data['building']={}
    data['smarket']={}
    dump()
    await ctx.send("Reset complete!")
    dump()   
     

#moderator/helper

@bot.command(aliases=["v","dem"])
@commands.has_role("Helpers")
async def demote(ctx):
  '''To demote yourself. <Helper>'''
  guildd=bot.get_guild(448888674944548874)
  role = discord.utils.get(guildd.roles, name="Helper")
  ath = str(ctx.author.id)
  await ctx.author.add_roles(role)
  role = discord.utils.get(guildd.roles, name="Helpers")
  await ctx.author.remove_roles(role)
  await ctx.send("You have been demoted , {}".format(ctx.author.mention))


@bot.command(aliases=["^","pro"])
@commands.has_role("Helper")
async def promote(ctx):
  '''To promote yourself. <Helper>'''
  guildd=bot.get_guild(448888674944548874)
  role = discord.utils.get(guildd.roles, name="Helpers")
  ath = str(ctx.author.id)
  await ctx.author.add_roles(role)
  role = discord.utils.get(guildd.roles, name="Helper")
  await ctx.author.remove_roles(role)
  await ctx.send("You have been promoted , {}".format(ctx.author.mention))


@bot.command()
@commands.has_role("Helpers")
async def poll(ctx,*,message):
    '''Creates a poll with yes or no. <Helper>'''
    poll = discord.Embed(colour=discord.Colour.blurple())
    poll.set_author(name="POLL")
    poll.add_field(name="Reg:- ",value=message,inline="false")
    reac="\U0001f44d"
    reac2="\U0001f44e"
    reac3="⛔"
    a=await ctx.send(embed=poll)
    await a.add_reaction(reac)
    await a.add_reaction(reac2)
    await a.add_reaction(reac3)

@bot.command()
@commands.has_role("Helpers")
async def kick(ctx,member:discord.Member):
    '''To kick a person out of the server. <Helper>'''
    await member.kick()
    await ctx.send("{} has been kicked from the server.".format(member.mention))

@bot.command()
@commands.has_role("Helpers")
async def ban(ctx,member:discord.Member):
    '''To ban a person from the server. <Helper>'''
    await member.ban()
    await ctx.send("{} has been banned from the server.".format(member.mention))
    
@bot.command(aliases=["rc"])
@commands.has_role("Helpers")
async def removecash(ctx,member:discord.Member,cash):
    '''Removes a certain amount of cash from a person. <Helper>'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    data['money'][str(member.id)]-=int(cash)
    await ctx.send("{} has been reduced from {}'s account. Current balance is {} .".format(cash,member.mention,data['money'][str(member.id)]))
    
@bot.command(aliases=["ac"])
@commands.has_role("Helpers")
async def addcash(ctx,member:discord.Member,cash):
    '''Adds a certain amount of cash to a person's balance. <Helper>'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    data['money'][str(member.id)]+=int(cash)
    await ctx.send("{} has been added to {}'s account. Current balance is {} .".format(cash,member.mention,data['money'][str(member.id)]))
    
@bot.command(aliases=["gso"])
@commands.has_role("Helpers")
async def opensignups(ctx):
    '''Opens signups. <Helpers>'''
    global gamestate
    gamestate = 1
    data['gamestate']=gamestate
    sgchannel=bot.get_channel(739400216146477137)
    guildd=ctx.message.guild
    role0 = discord.utils.get(guildd.roles, name="Helpers")
    await sgchannel.set_permissions(guildd.default_role, read_messages=True,send_messages=True)
    await sgchannel.set_permissions(role0, read_messages=True,send_messages=True)
    await ctx.send("Signups open!")
    await bot.change_presence(activity=discord.Game(name="Signups open!", type=1))
    dump()
    
@bot.command(aliases=["gsc"])
@commands.has_role("Helpers")
async def closesignups(ctx):
    '''Closes signups. <Helpers>'''
    global gamestate
    gamestate = 2
    data['gamestate']=gamestate
    sgchannel=bot.get_channel(739400216146477137)
    guildd=ctx.message.guild
    role0 = discord.utils.get(guildd.roles, name="Helpers")
    await sgchannel.set_permissions(guildd.default_role,read_messages=True,send_messages=False)
    await sgchannel.set_permissions(role0, read_messages=True,send_messages=True)
    await ctx.send("Signups closed!")
    await bot.change_presence(activity=discord.Game(name="Signups are closed.A game will soon begin.", type=1))
    dump()
    
@bot.command(aliases=["s"])
@commands.has_role("Helpers")
async def start(ctx,code:str,num=0):
    '''Starts the game (Type a number after s to run the assignroles command automatically) <Helpers>'''
    global gamestate
    global data
    if int(gamestate)!=2:
        await ctx.send("Check the gamestate.")
        return
    if data['roles'] == []:
        await ctx.send("Role list is empty....")
        return
    gamestate=3
    data['gamestate']=gamestate
    data['code']['gamecode']=str(code)
    await ctx.send("Game has started with code {} !".format(code))
    await bot.change_presence(activity=discord.Game(name="Game running.", type=1))
    data['players']={}
    data['code']['ccno']=0
    for user in data['signedup']:
        data['players'][user]={}
        data['players'][user]['incc']=[]
        guildd=bot.get_guild(448888674944548874)
        userr=discord.utils.get(guildd.members,id=int(user))
        role = discord.utils.get(guildd.roles, name="Signed-Up!")
        await userr.remove_roles(role)
        guildd=bot.get_guild(448888674944548874)
        role = discord.utils.get(guildd.roles, name="Players")
        await userr.add_roles(role)
        role = discord.utils.get(guildd.roles, name="Alive")
        await userr.add_roles(role)
    if num !=0:
        await assignroles(ctx,code)
    dump()
        
@bot.command(aliases=["as"])
@commands.has_role("Helpers")
async def assignroles(ctx,code):
    '''Assigns roles and makes all channels. <Helpers>'''
    global data
    if int(gamestate) != 3:
        await ctx.send("The game hasn't started")
        return
    listoplayers = []
    rolelist=[]
    #
    guildd=ctx.message.guild
    role0 = discord.utils.get(guildd.roles, name="Helpers") 
    role1 = discord.utils.get(guildd.roles, name="Alive")
    role2 = discord.utils.get(guildd.roles, name="Respawning")
    role3 = discord.utils.get(guildd.roles, name="Dead")
    role4 = discord.utils.get(guildd.roles, name="Spectator")
    storymark = {
    guildd.default_role: discord.PermissionOverwrite(read_messages=False),
    guildd.me: discord.PermissionOverwrite(read_messages=True),
    role0: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role1: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role2: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role3: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role4: discord.PermissionOverwrite(read_messages=True,send_messages=False)
                 }
    batle = {
    guildd.default_role: discord.PermissionOverwrite(read_messages=False),
    guildd.me: discord.PermissionOverwrite(read_messages=True),
    role0: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role1: discord.PermissionOverwrite(read_messages=True,send_messages=True,add_reactions=True),
    role2: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role3: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role4: discord.PermissionOverwrite(read_messages=True,send_messages=False)
                 }
    resp = {
    guildd.default_role: discord.PermissionOverwrite(read_messages=False),
    guildd.me: discord.PermissionOverwrite(read_messages=True),
    role0: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role1: discord.PermissionOverwrite(read_messages=False,send_messages=False,add_reactions=True),
    role2: discord.PermissionOverwrite(read_messages=True,send_messages=True,add_reactions=True),
    role3: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role4: discord.PermissionOverwrite(read_messages=True,send_messages=False)
                 }
    deads = {
    guildd.default_role: discord.PermissionOverwrite(read_messages=False),
    guildd.me: discord.PermissionOverwrite(read_messages=True),
    role0: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role1: discord.PermissionOverwrite(read_messages=False,send_messages=False,add_reactions=True),
    role2: discord.PermissionOverwrite(read_messages=False,send_messages=False,add_reactions=True),
    role3: discord.PermissionOverwrite(read_messages=True,send_messages=True,add_reactions=True),
    role4: discord.PermissionOverwrite(read_messages=True,send_messages=True,add_reactions=True)
                 }
    namee = str(data['code']['gamecode'])
    await guildd.create_category(namee)
    cate = discord.utils.get(ctx.message.guild.categories, name=namee)
    story = await guildd.create_text_channel('story-time',overwrites=storymark,category=cate)
    batlec = await guildd.create_text_channel('battlefield',overwrites=batle,category=cate)
    markc = await guildd.create_text_channel('market',overwrites=storymark,category=cate)
    respc = await guildd.create_text_channel('respawning',overwrites=resp,category=cate)      
    deadsc = await guildd.create_text_channel('dead-spec',overwrites=deads,category=cate) 
    await batlec.send("This is the battlefield! Where warriors fight to death! \n Or somethimes like to chill out and chat.")
    #
    guildd=ctx.message.guild
    role0 = discord.utils.get(guildd.roles, name="Helpers")
    role3 = discord.utils.get(guildd.roles, name="Dead")
    role4 = discord.utils.get(guildd.roles, name="Spectator")
    overwrites = {
    guildd.default_role: discord.PermissionOverwrite(read_messages=False),
    guildd.me: discord.PermissionOverwrite(read_messages=True),
    role0: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role3: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role4: discord.PermissionOverwrite(read_messages=True,send_messages=False)
                 }
    namee = str(data['code']['gamecode'])+' factions'
    await guildd.create_category(namee)
    cate = discord.utils.get(ctx.message.guild.categories, name=namee)
    red = await guildd.create_text_channel('red',overwrites=overwrites,category=cate)
    blue = await guildd.create_text_channel('blue',overwrites=overwrites,category=cate)
    green = await guildd.create_text_channel('green',overwrites=overwrites,category=cate)
    yellow = await guildd.create_text_channel('yellow',overwrites=overwrites,category=cate)
    data['building']['red']={}
    data['building']['blue']={}
    data['building']['green']={}
    data['building']['yellow']={}
    data['building']['red']['vault']=0
    data['building']['blue']['vault']=0
    data['building']['green']['vault']=0
    data['building']['yellow']['vault']=0
    data['building']['red']['forge']=1
    data['building']['blue']['forge']=1
    data['building']['green']['forge']=1
    data['building']['yellow']['forge']=1
    #
    teamred=discord.Embed(colour=discord.Colour.red())
    teamred.set_author(name="Team info!")
    teamred.add_field(name="Welcome!",value="You are all members of the red team! \n Work together and win this game!")
    await red.send(embed=teamred)
    teamblue=discord.Embed(colour=discord.Colour.blue())
    teamblue.set_author(name="Team info!")
    teamblue.add_field(name="Welcome!",value="You are all members of the blue team! \n Work together and win this game!")
    await blue.send(embed=teamblue)
    teamgreen=discord.Embed(colour=discord.Colour.green())
    teamgreen.set_author(name="Team info!")
    teamgreen.add_field(name="Welcome!",value="You are all members of the green team! \n Work together and win this game!")
    await green.send(embed=teamgreen)
    teamyellow=discord.Embed(colour=discord.Colour.gold())
    teamyellow.set_author(name="Team info!")
    teamyellow.add_field(name="Welcome!",value="You are all members of the yellow team! \n Work together and win this game!")
    await yellow.send(embed=teamyellow)
    #
    '''await red.send("```You are all members of the red team! \n Work together and win this game!```")
    await blue.send("```You are all members of the blue team! \n Work together and win this game!```")
    await green.send("```You are all members of the green team! \n Work together and win this game!```")
    await yellow.send("```You are all members of the yellow team! \n Work together and win this game!```")'''
    #
    for player in data['players']:
        listoplayers.append(player)
        #print(listoplayers)
    for role in data['roles']:
        rolelist.append(role)
        #print(listoplayers)
    countp=len(listoplayers)
    countr=len(rolelist)
    num=0
    while num<countp:
        user = random.choice(listoplayers)
        listoplayers.remove(user)
        role= random.choice(rolelist)
        rolelist.remove(role)
        data['players'][user]['role']=role
        data['players'][user]['team']=data['rt'][role]['team']
        data['players'][user]['state']=1
        #state 1 is alive ,0 is dead
        #print(data)
        num+=1
    #print(data)
    #
    for user in data['players']:
        guildd=bot.get_guild(448888674944548874)
        userr=discord.utils.get(guildd.members,id=int(user))
        roleinfo=discord.Embed(colour=discord.Colour.red())
        roleinfo.set_author(name="Role info!")
        roleinfo.add_field(name="This message has been sent to you to inform you of the role you have in the next up coming game in the Colour Battles server!",value="**Your role for this game is `{}` and you are in the team `{}`!** \n You are **__not__** allowed to share this message! \n You are **__not__** allowed to share the screenshot of this message! \n Breaking any of these rules can result in you being banned from the server.".format(data['players'][user]['role'],data['players'][user]['team']),inline="false")
        roleinfo.add_field(name="If you need help reagrding this role or this game , please make sure to contact the Informers or the Helpers or read the role info from from the #role_info channel.",value="Have a good game!\n *I am a bot and this action has been done automatically. Please contact the informer if anything is unclear.* ",inline="false")
        await userr.send(embed=roleinfo)
        if data['players'][user]['team']=="red":
            await red.set_permissions(userr, read_messages=True,send_messages=True,add_reactions=True)
            data['players'][str(user)]['incc'].append(red.id)
        elif data['players'][user]['team']=="blue":
            await blue.set_permissions(userr, read_messages=True,send_messages=True,add_reactions=True)
            data['players'][str(user)]['incc'].append(blue.id)
        elif data['players'][user]['team']=="green":
            await green.set_permissions(userr, read_messages=True,send_messages=True,add_reactions=True)
            data['players'][str(user)]['incc'].append(green.id)
        elif data['players'][user]['team']=="yellow":
            await yellow.set_permissions(userr, read_messages=True,send_messages=True,add_reactions=True)
            data['players'][str(user)]['incc'].append(yellow.id)
        else:
            data['building'][str(user)]={}
            data['building'][str(user)]['forge']=5
        roleid= data['players'][user]['role']
        rolename=data['rt'][roleid]['lirole']
        chnlname = str(data['players'][user]['team']) + "_" + str(rolename)
        chnl = await guildd.create_text_channel(chnlname,overwrites=overwrites,category=cate)
        await chnl.set_permissions(userr, read_messages=True,send_messages=True,add_reactions=True)
        role = data['players'][user]['role']
        rolet=data['rt'][str(role)]['lirole']
        await rolehelp(rolet,chnl)
        #data['players'][str(user)]['incc'].append(chnl.id) THIS DISABLES PEOPLE FROM TALKING IN CHAT WHEN DEAD
    await listallr(ctx)
    dump()    
    
@bot.command(aliases=["a"])
@commands.has_role("Helpers")
async def listallr(ctx):
    '''Lists everyone's roles. <Helpers>'''
    temp = ""
    for user in data['players']:
        guildd=bot.get_guild(448888674944548874)
        userr=discord.utils.get(guildd.members,id=int(user))
        temp +="{} has the role `{}` \n".format(userr.mention,data['players'][user]['role'])
    msg = await ctx.send("Loading.")
    await msg.edit(content=temp)


@bot.command(aliases=["ar"])
@commands.has_role("Helpers")
async def addrole(ctx,role,team,*,litrole):
    '''Adds roles to the role list.(Similar roles must be entered with a number after them , teams can only be red , blue , green or yellow.(No Caps) Any other team will be considered as a solo team) <Helpers>'''
    if (int(gamestate) >= 3):
        await ctx.send("A game is already going on.")
        return
    data['roles'].append(role)
    data['rt'][role]={}
    data['rt'][role]['team']=team
    data['rt'][role]['lirole'] = litrole
    await ctx.send("{} added for the team {}.".format(role,team))
    dump()
    
@bot.command(aliases=["rr"])
@commands.has_role("Helpers")
async def removerole(ctx,role,team):
    '''Removes a role from the role list. <Helpers>'''
    if (int(gamestate) >= 3):
        await ctx.send("A game is already going on.")
        return
    data['roles'].remove(role)
    #data['rt'].remove(role)
    del data['rt'][role]
    await ctx.send("{} removed.".format(role))
    dump()
   
@bot.command(aliases=["lr"])
@commands.has_role("Helpers")
async def listroles(ctx):
    '''Prints the entire role list. <Helpers>'''
    temp = ""
    await ctx.send("The rolelist is - ")
    for role in data['roles']:
        temp +="{} of {}\n".format(role,data['rt'][role])
    msg = await ctx.send("Loading.")
    await msg.edit(content=temp)
    
@bot.command(aliases=["cr"])
@commands.has_role("Helpers")
async def clearroles(ctx):
    '''Removes all roles from the list. <Helpers>'''
    if (int(gamestate) >= 3):
        await ctx.send("A game is already going on.")
        return
    data['roles']=[]
    data['rt']={}
    await ctx.send("Cleared.")
    dump()

@bot.command(aliases=["eg"])
@commands.has_role("Helpers")
async def endgame(ctx):
    '''Ends the game. <Helpers>'''
    global gamestate
    if int(gamestate)!=3:
        await ctx.send("A game isn't even going on.")
        return
    gamestate=4
    data['gamastate']=4
    await bot.change_presence(activity=discord.Game(name="Game concluded!", type=1))
    for user in data['players']:
        guildd=bot.get_guild(448888674944548874)
        userr=discord.utils.get(guildd.members,id=int(user))
        role = discord.utils.get(guildd.roles, name="Spectator")
        await userr.add_roles(role)
    await ctx.send("The game has ended!")
    dump()
    
@bot.command(aliases=["k"])
@commands.has_role("Helpers")
async def kill(ctx,user:discord.Member):
    '''Sets a person's status as respawning in game. <Helpers>'''
    if int(gamestate)!=3:
        await ctx.send("There isn't a game going on.")
        return
    data['players'][str(user.id)]['state']=0
    guildd=bot.get_guild(448888674944548874)
    role = discord.utils.get(guildd.roles, name="Respawning")
    await user.add_roles(role)
    role = discord.utils.get(guildd.roles, name="Alive")
    await user.remove_roles(role)
    for cc in data['players'][str(user.id)]['incc']:
        chnl = bot.get_channel(int(cc))
        await chnl.set_permissions(user, read_messages=True,send_messages=False,add_reactions=False)
    await ctx.send("Killed {}.".format(user.mention))
    dump()
    
@bot.command(aliases=["re"])
@commands.has_role("Helpers")
async def respawn(ctx,user:discord.Member):
    '''Respawns a person in game <Helpers>'''
    if int(gamestate)!=3:
        await ctx.send("There isn't a game going on.")
        return
    data['players'][str(user.id)]['state']=1
    guildd=bot.get_guild(448888674944548874)
    role = discord.utils.get(guildd.roles, name="Respawning")
    await user.remove_roles(role)
    role = discord.utils.get(guildd.roles, name="Alive")
    await user.add_roles(role)
    for cc in data['players'][str(user.id)]['incc']:
        chnl = bot.get_channel(int(cc))
        await chnl.set_permissions(user, read_messages=True,send_messages=True,add_reactions=True)
    await ctx.send("Respawned {}.".format(user.mention))
    dump()

@bot.command(aliases=["pk"])
@commands.has_role("Helpers")
async def pkill(ctx,user:discord.Member):
    '''Kills a person permanently in game. <Helpers>'''
    if int(gamestate)!=3:
        await ctx.send("There isn't a game going on.")
        return
    data['players'][str(user.id)]['state']=0
    guildd=bot.get_guild(448888674944548874)
    role = discord.utils.get(guildd.roles, name="Respawning")
    await user.remove_roles(role)
    role = discord.utils.get(guildd.roles, name="Alive")
    await user.remove_roles(role)
    role = discord.utils.get(guildd.roles, name="Dead")
    await user.add_roles(role)
    for cc in data['players'][str(user.id)]['incc']:
        chnl = bot.get_channel(int(cc))
        await chnl.set_permissions(user, read_messages=True,send_messages=False,add_reactions=False)
    await ctx.send("Permanently killed {}.".format(user.mention))
    dump()


@bot.command(aliases=["mg"])
@commands.has_role("Helpers")
async def massgive(ctx,cash=100):
  '''Gives a certain amount of cash to everyone who has an account. <Helpers>'''
  global data
  if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  for  ath in data['money']:
    if data['players'][ath]['team']=="solo":
      add=cash*data['building'][ath]['forge']
    else:
      team=str(data['players'][ath]['team'])
      add=cash*data['building'][team]['forge']
    data['money'][ath]+=int(add)
  await ctx.send("Added the cash to everyone who had an account.")
  dump()

@bot.command(aliases=["mbal"])
@commands.has_role("Helpers")
async def masterbalance(ctx,member:discord.Member):
  '''Allows to see the balance of another player <Helpers>'''
  if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  id=str(member.id)
  await ctx.send("{}'s balance is {}.".format(member.mention,data['money'][id]))

@bot.command(aliases=["ca"])
@commands.has_role("Helpers")
async def createauction(ctx,name,*,text):
    '''Allows the user to create a auction <Helpers>'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    global data
    guildd=bot.get_guild(448888674944548874)
    mark=discord.utils.get(guildd.channels,name="market")
    data['auction']['state']=1
    await mark.send("__**ITEM - {}**__".format(name))
    await mark.send("Perks - {}".format(text))
    aucmsg = await mark.send("Current bid - ")
    data['auction']['msg']=str(aucmsg.id)
    data['auction']['chn']=str(aucmsg.channel.id)
    data['auction']['bid']=0
    data['auction']['bider']=""
    dump()

@bot.command(aliases=["cla"])
@commands.has_role("Helpers")
async def closeauction(ctx):
  '''Allows the user to close a auction <Helpers>'''
  if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  global data
  if data['auction']['state']==0:
    await ctx.send("There is no auction going on right now.")
    return
  while 1==1:
    a=data['auction']['bid']
    await asyncio.sleep(30)
    if a==data['auction']['bid']:
      break

  data['auction']['state']=0
  who=data['auction']['bider']
  cost=data['auction']['bid']
  guildd=bot.get_guild(448888674944548874)
  mark=discord.utils.get(guildd.channels,name="market")
  await mark.send("Congrats! <@{}> has won the item auctioned for {} ! ".format(who,cost))
  data['money'][str(who)]-=cost
  data['auction']['msg']=""
  data['auction']['chn']=""
  data['auction']['bid']=0
  data['auction']['bider']=""
  dump()

@bot.command(aliases=["rmm"])
@commands.has_role("Helpers")
async def resetstockmarket(ctx):
  '''Use this to start stock market'''
  if int(gamestate)!=3:
    await ctx.send("There is no game going on right now.")
    return
  global data
  data['smarket']['state']=1
  data['smarket']['inv']={}
  data['smarket']['stocks']={}
  data['smarket']['stocks']['sun']=0
  data['smarket']['stocks']['smirk']=0
  data['smarket']['stocks']['smile']=0
  data['smarket']['stocks']['joy']=0
  data['smarket']['stocks']['pens']=0
  data['smarket']['trades']={}
  data['smarket']['trades']['sun']=0
  data['smarket']['trades']['smirk']=0
  data['smarket']['trades']['smile']=0
  data['smarket']['trades']['joy']=0
  data['smarket']['trades']['pens']=0
  #try:
  guildd=bot.get_guild(448888674944548874)
  channel=bot.get_channel(int(data['smarket']['chn']))
  msgid = int(data['smarket']['msg'])
  msg = await channel.fetch_message(msgid)
  await msg.delete()
  #except:
    #await ctx.send("There wasn't a market.")
  data['smarket']['msg']=""
  data['smarket']['chn']=""
  await ctx.send("I've reset the stock market.")
  dump()


@bot.command(aliases=["tmm"])
@commands.has_role("Helpers")
async def togglestockmarket(ctx):
  '''Use this to turn on or turn off the stock market <Helpers>'''
  if int(gamestate)!=3:
    await ctx.send("There is no game going on right now.")
    return
  global data
  if data['smarket']['state']==1:
    data['smarket']['state']=0
    await ctx.send("Closed.")
  elif data['smarket']['state']==0:
    data['smarket']['state']=1
    await ctx.send("Opened.")
  dump()

@bot.command(aliases=["cmm"])
@commands.has_role("Helpers")
async def createstockmarket(ctx):
  '''Use this to start stock market'''
  if int(gamestate)!=3:
    await ctx.send("There is no game going on right now.")
    return
  global data
  data['smarket']['state']=1
  data['smarket']['inv']={}
  data['smarket']['stocks']={}
  data['smarket']['stocks']['sun']=1000
  data['smarket']['stocks']['smirk']=500
  data['smarket']['stocks']['smile']=100
  data['smarket']['stocks']['joy']=50
  data['smarket']['stocks']['pens']=10
  data['smarket']['trades']={}
  data['smarket']['trades']['sun']=0
  data['smarket']['trades']['smirk']=0
  data['smarket']['trades']['smile']=0
  data['smarket']['trades']['joy']=0
  data['smarket']['trades']['pens']=0
  guildd=bot.get_guild(448888674944548874)
  mark=discord.utils.get(guildd.channels,name="market")
  smarket = await mark.send("Cost of :sunglasses: is 1000 \nCost of :smirk: is 500 \nCost of :smiley: is 100 \nCost of :joy: is 50 \nCost of :pensive: is 10 \n")
  await smarket.pin()
  data['smarket']['msg']=str(smarket.id)
  data['smarket']['chn']=str(smarket.channel.id)
  dump()

@bot.command(aliases=["chngmm"])
@commands.has_role("Helpers")
async def changestockmarket(ctx):
    '''Use this to manually change stock market prices <Helpers>'''
    global data
    if int(gamestate)!=3:
      return
    try:
      if data['smarket']['state']==0:
        return
      guildd=bot.get_guild(448888674944548874)
      channel=bot.get_channel(int(data['smarket']['chn']))
      msgid = int(data['smarket']['msg'])
      msg = await channel.fetch_message(msgid)
      await change()
      a=data['smarket']['stocks']['sun']
      b=data['smarket']['stocks']['smirk']
      c=data['smarket']['stocks']['smile']
      d=data['smarket']['stocks']['joy']
      e=data['smarket']['stocks']['pens']
      await msg.edit(content="Cost of :sunglasses: is {} \nCost of :smirk: is {} \nCost of :smiley: is {} \nCost of :joy: is {} \nCost of :pensive: is {} \n".format(a,b,c,d,e))
      await ctx.send("Changed.")
    except:
      await ctx.send("Failed")
      return

#\:sunglasses:\:smirk:\:smiley:\:joy:\:pensive:
#all
@bot.command()
async def ping(ctx):
    '''Returns Pong.'''
    print("Pong!")
    await ctx.send("Pong!")
    dump()
    
@bot.command(aliases=["j","join"])
async def signup(ctx):
    '''Allows you to signup for a game.Sign out by typing the command again.'''
    global data
    if (int(gamestate) != 1):
        await ctx.send("Sign ups are closed right now. Try joining when they are open , of after the game has concluded. Contact a Informer or a helper if you need help.")
        return
    ath=str(ctx.author.id) 
    if not ath in data['signedup']:
      if not ath in data['specters']:
        data['signedup'][ath] = 1
        guildd=bot.get_guild(448888674944548874)
        role = discord.utils.get(guildd.roles, name="Signed-Up!")
        await ctx.send("You have been signed-up! :thumbsup:")
        await ctx.author.add_roles(role)
        dump()
      else:
        await ctx.send("You are currently spectating. Kindly stop spectating if you want to play.")
    else:
        data['signedup'].pop(ath)
        guildd=bot.get_guild(448888674944548874)
        role = discord.utils.get(guildd.roles, name="Signed-Up!")
        await ctx.send("You have been signed-out!")
        await ctx.author.remove_roles(role)
        dump()
    
@bot.command(aliases=["sl"])
async def slist(ctx):
    '''Shows a list of everyone signed up.'''
    temp = ""
    tempno=0
    temp+="The list of people signed-up is - \n"
    for member in data['signedup']:
        tempno+=1
        temp +="<@{}> \n".format(member)
    temp += "The number of people signed up is {} \n".format(tempno)
    msg = await ctx.send("Loading.")
    await msg.edit(content=temp)
    
@bot.command(aliases=["sp","spec"])
async def spectate(ctx):
    '''Allows you to spectate the game.'''
    global data
    if int(gamestate)==0:
        await ctx.send("You cannot use this command right now.")
        return
    guildd=bot.get_guild(448888674944548874)
    role = discord.utils.get(guildd.roles, name="Spectator")
    ath = str(ctx.author.id)
    if not ath in data['specters']:
      if not ath in data['signedup']:
        await ctx.author.add_roles(role)
        data['specters'].append(ath)
        await ctx.send("You are now spectating! ")
      else:
        await ctx.send("You have signed up for a game. Please sign out before spectating.")
    else:
      await ctx.author.remove_roles(role)
      data['specters'].remove(ath)
      await ctx.send("You are no longer spectating! ")
    dump()
    
@bot.command(aliases=["c"])
async def bal(ctx):
    '''Prints your balance.'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    await ctx.send("{}'s bank balance is {}".format(ctx.author.mention,data['money'][str(ctx.author.id)]))
   
@bot.command(aliases=["fghs"])
@commands.has_role("Respawning")
async def freeghostsay(ctx,*,msg):
    '''Use to send messages into town hall as a ghost for free!! <Respawning>'''
    guildd=bot.get_guild(448888674944548874)
    townc=discord.utils.get(guildd.channels,name="battlefield")
    taboo = "@everyone"
    if taboo in str(msg):
      await ctx.send("Please don't ping @ everyone.")
    else:
      alpha=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','1','2','3','4','5','6','7','8','9','0']
      fmsg=msg.replace(random.choice(alpha),'o')
      fmsg=fmsg.replace(random.choice(alpha),'o')
      fmsg=fmsg.replace(random.choice(alpha),'o')
      fmsg=fmsg.replace(random.choice(alpha),'o')
      fmsg=fmsg.replace(random.choice(alpha),'o')
      fmsg=fmsg.replace(random.choice(alpha),'p')
      fmsg=fmsg.replace(random.choice(alpha),'p')
      fmsg=fmsg.replace(random.choice(alpha),'.')
      fmsg=fmsg.replace(random.choice(alpha),'.')
      fmsg=fmsg.replace(random.choice(alpha),'OOOO')
      fmsg=fmsg.replace(random.choice(alpha),'OOOO')
      await townc.send("<Ghost> {}".format(fmsg))
    '''ghosthook = Webhook('https://discordapp.com/api/webhooks/723763897764675616/9c5GmG9WKemUjWv4cEMGVfHrjjmExGvV36JmS38Hep5KqK4nOKYfayzr6OTIQa2rgZ_O')
    ghosthook.send(msg)'''
   
@bot.command(aliases=["ghs"])
@commands.has_role("Respawning")
async def ghostsay(ctx,*,msg):
    '''Use to send messages into town hall as a ghost for a price of 10c <Respawning>'''
    global data
    guildd=bot.get_guild(448888674944548874)
    townc=discord.utils.get(guildd.channels,name="battlefield")
    taboo = "@everyone"
    if taboo in str(msg):
      await ctx.send("Please don't ping @ everyone.")
    else:
      ath=str(ctx.author.id)
      data['money'][ath]-=10
      await townc.send("<Ghost> {}".format(msg))
    dump()

@bot.command(aliases=["cc"])
@commands.has_role("Alive")
async def createchannel(ctx,ccname,*member:discord.Member):
    '''Used to create a communication channel.'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    global data
    guildd=ctx.message.guild
    if int(gamestate)!=3:
        await ctx.send("There isn't a game going on.")
        return
    if data['money'][str(ctx.author.id)] <50:
        await ctx.send("You cannot afford to make a cc....")
        await ctx.message.delete()
        return
    for people in member:
      if data['players'][str(people.id)]['state']==0:
        await ctx.send("You cannot make ccs with the dead.")
        return
    if data['code']['ccno'] ==0:
      name=data['code']['gamecode'] +' cc1'
      await guildd.create_category(name)
    elif data['code']['ccno']==50:
      name=data['code']['gamecode'] +' cc2'
      await guildd.create_category(name)
    elif data['code']['ccno']==100:
      name=data['code']['gamecode'] +' cc3'
      await guildd.create_category(name)
    elif data['code']['ccno']==150:
      name=data['code']['gamecode'] +' cc4'
      await guildd.create_category(name)
    elif data['code']['ccno']==200:
      name=data['code']['gamecode'] +' cc5'
      await guildd.create_category(name)
    data['money'][str(ctx.author.id)] -= 50
    author = ctx.message.author
    role0 = discord.utils.get(guildd.roles, name="Helpers")
    '''role1 = discord.utils.get(guildd.roles, name="Alive")
    role2= discord.utils.get(guildd.roles, name="Spectatators")'''
    role3 = discord.utils.get(guildd.roles, name="Dead")
    role4 = discord.utils.get(guildd.roles, name="Spectator")
    #
    if data['code']['ccno']<50:
      name=data['code']['gamecode'] +' cc1'
      cate = discord.utils.get(ctx.message.guild.categories, name=name)
    elif data['code']['ccno']<100:
      name=data['code']['gamecode'] +' cc2'
      cate = discord.utils.get(ctx.message.guild.categories, name=name)
    elif data['code']['ccno']<150:
      name=data['code']['gamecode'] +' cc3'
      cate = discord.utils.get(ctx.message.guild.categories, name=name)
    elif data['code']['ccno']<200:
      name=data['code']['gamecode'] +' cc4'
      cate = discord.utils.get(ctx.message.guild.categories, name=name)
    elif data['code']['ccno']<250:
      name=data['code']['gamecode'] +' cc5'
      cate = discord.utils.get(ctx.message.guild.categories, name=name)
    data['code']['ccno']+=1
    overwrites = {
    guildd.default_role: discord.PermissionOverwrite(read_messages=False),
    guildd.me: discord.PermissionOverwrite(read_messages=True),
    author:discord.PermissionOverwrite(read_messages=True,add_reactions=True),
    #member:discord.PermissionOverwrite(read_messages=True,add_reactions=True),
    role0:discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role3:discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role4:discord.PermissionOverwrite(read_messages=True,send_messages=False)
                 }
    a = await guildd.create_text_channel(str(ccname),overwrites=overwrites,category=cate)
    plist=""
    plist+="<@{}> \n".format(author.id)
    for people in member:
      await a.set_permissions(people, read_messages=True,send_messages=True)
      data['players'][str(people.id)]['incc'].append(a.id)
      plist+="<@{}> \n".format(people.id)
    print(a.id)
    await a.send("This is a new cc made by {} :- \n Participants:- \n {}".format(author.mention,plist))
    data['chnls'][str(a.id)]={}
    data['chnls'][str(a.id)]['owner']=ctx.author.id
    data['players'][str(ctx.author.id)]['incc'].append(a.id)
    await ctx.message.delete()
    dump()

@bot.command(aliases=["add"])
@commands.has_role("Alive")
async def addinchannel(ctx,member:discord.Member):
    '''Adds a person to the channel'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    if data['players'][str(member.id)]['state']==0:
        await ctx.send("You add a dead person to the cc.")
        return
    chnl = ctx.channel.id
    if data['chnls'][str(chnl)]['owner'] == ctx.author.id:
        await ctx.channel.set_permissions(member, read_messages=True,send_messages=True)
        data['players'][str(member.id)]['incc'].append(chnl)
        await ctx.send("Welcome , {} !".format(member.mention))
    else:
        await ctx.send("You probably aren't the owner of this cc.")
        
@bot.command(aliases=["remove"])
@commands.has_role("Alive")
async def removeinchannel(ctx,member:discord.Member):
    '''Removes a person from the channel'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    if data['players'][str(member.id)]['state']==0:
        await ctx.send("Only remove people if they are alive.")
        return
    chnl = ctx.channel.id
    if data['chnls'][str(chnl)]['owner'] == ctx.author.id:
        await ctx.channel.set_permissions(member, read_messages=False,send_messages=False)
        data['players'][str(member.id)]['incc'].remove(chnl)
        await ctx.send("Removed {} from the cc.".format(member.mention))
    else:
        await ctx.send("You probably aren't the owner of this cc.")

@bot.command(aliases=["sm"])
@commands.has_role("Alive")
async def sendmoney(ctx,member:discord.Member,cash):
  '''Allows alive players to send money to others.'''
  ath=str(ctx.message.author.id)
  if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  if int(cash) < 0:
    await ctx.send("You cannot send negative money.")
    return
  if data['money'][ath] < int(cash):
    await ctx.send("You do not have that many coins in your account.")
    return
  data['money'][ath]-=int(cash)
  per=str(member.id)
  data['money'][per]+=int(cash)
  await ctx.send("Done. Sent {} to {} from {}'s account.".format(cash,member.mention,ctx.author.mention))

@bot.command(aliases=["al"])
async def alivelist(ctx):
  '''Shows all alive players.'''
  if int(gamestate) != 3:
    await ctx.send("There is no game going on right now.")
    return
  temp = ""
  temp+="All alive players are- \n"
  al=0
  for member in data['players']:
    if data['players'][member]['state']==1:
      temp +="<@{}> \n".format(member)
      al+=1
  temp+="The number of alive players are- {} \n".format(al)
  msg = await ctx.send("Loading.")
  await msg.edit(content=temp)

@bot.command(aliases=["b"])
@commands.has_role("Alive")
async def bid(ctx,cash:int):
  '''Allows the bid in the auction <King only>'''
  global data
  ath=str(ctx.author.id)
  if int(gamestate) != 3:
    await ctx.send("There is no game going on right now.")
    return
  if data['auction']['state']==0:
    await ctx.send("There is no auction going on right now.")
    return
  role = data['players'][ath]['role']
  rolet=data['rt'][role]['lirole']
  '''if rolet!="king" and rolet!="prince": #fix
    await ctx.send("You are not a king. Please only use this command if your role is King.")
    return'''
  await ctx.message.delete()
  if cash>data['money'][ath]:
    await ctx.send("You can only bid what you have.")
    return
  if cash <= data['auction']['bid']:
    await ctx.send("The current bid is higher than what you're currently offering.")
    return
  data['auction']['bid']=cash
  '''if data['players'][ath]['team'] =="red":
    who= "Red King."
  elif data['players'][ath]['team'] =="blue":
    who= "Blue King."
  elif data['players'][ath]['team'] =="green":
    who= "Green King."
  elif data['players'][ath]['team'] =="yellow":
    who= "Yellow King."
  else:
    who = "Unknown bidder"'''
  who=str(ctx.author.id)
  data['auction']['bider']=who
  guildd=bot.get_guild(448888674944548874)
  channel=bot.get_channel(int(data['auction']['chn']))
  msgid = int(data['auction']['msg'])
  msg = await channel.fetch_message(msgid)
  await msg.edit(content="Current bid - {} by <@{}>".format(cash,who))
  dump()

@bot.command(aliases=["de"])
@commands.has_role("Alive")
async def deposit(ctx,cash:int):
  '''Helps you to deposit cash to your team's vault'''
  global data
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  if cash<0:
    await ctx.send("Cash can't be a negative value")
    return
  ath=str(ctx.author.id)
  team=data['players'][ath]['team']
  try:
    print(data['building'][team]['vault'])
  except:
    await ctx.send("You might not have a vault")
    return
  if cash>data['money'][ath]:
    await ctx.send("You do not have this much cash.")
    return
  data['building'][team]['vault']+=cash
  data['money'][ath]-=cash
  await ctx.send("Done! Money transferred.")
  dump()

@bot.command(aliases=["w"])
@commands.has_role("Alive")
async def withdraw(ctx,cash:int):
  '''Helps you to withdraw cash from your team's vault'''
  global data
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  if cash<0:
    await ctx.send("Cash can't be a negative value")
    return
  ath=str(ctx.author.id)
  team=data['players'][ath]['team']
  try:
    print(data['building'][team]['vault'])
  except:
    await ctx.send("You might not have a vault")
    return
  if cash>data['building'][team]['vault']:
    await ctx.send("Your vault doesn't hold this much cash.")
    return
  data['building'][team]['vault']-=cash
  data['money'][ath]+=cash
  await ctx.send("Done! Money transferred.")
  dump()

@bot.command(aliases=["va"])
@commands.has_role("Alive")
async def vault(ctx):
  '''Displays the amount of cash in your team's vault'''
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  ath=str(ctx.author.id)
  team=data['players'][ath]['team']
  try:
    money=data['building'][team]['vault']
  except:
    money=0
  await ctx.send("Your team's vault has {}".format(money))

@bot.command(aliases=["dif"])
@commands.has_role("Alive")
async def disforge(ctx):
  '''Displays your team's forge level.'''
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  ath=str(ctx.author.id)
  if data['players'][ath]['team']=="solo":
      forglvl=data['building'][ath]['forge']
  else:
      team=str(data['players'][ath]['team'])
      forglvl=data['building'][team]['forge']
  cost=int((forglvl*forglvl)*100)
  await ctx.send("Your team's forge is on level {}. The next upgrade costs {}.".format(forglvl,cost))

@bot.command(aliases=["upf"])
@commands.has_role("Alive")
async def upforge(ctx):
  '''Use this to upgrade your team's forge'''
  global data
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  ath=str(ctx.author.id)
  if data['players'][ath]['team']=="solo":
      forglvl=data['building'][ath]['forge']
  else:
      team=str(data['players'][ath]['team'])
      forglvl=data['building'][team]['forge']
  cost=int((forglvl*forglvl)*100)
  if data['money'][ath]<cost:
    await ctx.send("You cannot afford this upgrade.")
    return
  data['money'][ath]-=cost
  if data['players'][ath]['team']=="solo":
      data['building'][ath]['forge']+=1
  else:
      team=data['players'][ath]['team']
      data['building'][team]['forge']+=1
  await ctx.send("Upgrade successful.")
  dump()

@bot.command(aliases=["inv"])
@commands.has_role("Alive")
async def inventory(ctx):
  '''Use this to check your stock inventory.'''
  global data
  ath = str(ctx.author.id)
  if ath not in data['smarket']['inv']:
    data['smarket']['inv'][ath]={}
    data['smarket']['inv'][ath]['sun']=0
    data['smarket']['inv'][ath]['smirk']=0
    data['smarket']['inv'][ath]['smile']=0
    data['smarket']['inv'][ath]['joy']=0
    data['smarket']['inv'][ath]['pens']=0
  a=data['smarket']['inv'][ath]['sun']
  b=data['smarket']['inv'][ath]['smirk']
  c=data['smarket']['inv'][ath]['smile']
  d=data['smarket']['inv'][ath]['joy']
  e=data['smarket']['inv'][ath]['pens']
  await ctx.send("You have- \n {} of :sunglasses: \n {} of :smirk: \n {} of :smiley: \n {} of :joy: \n {} of :pensive: ".format(a,b,c,d,e))
  dump()

@bot.command(aliases=["by"])
@commands.has_role("Alive")
async def buy(ctx,thing,num:int=1):
  '''Use this to buy any stocks.'''
  if int(gamestate)!=3:
    await ctx.send("There is no game going on right now.")
    return
  if data['smarket']['state']==0:
    await ctx.send("Market is closed.")
    return
  if num<0:
    await ctx.send("Number cannot be nagative.")
    return
  ath=str(ctx.author.id)
  if ath not in data['smarket']['inv']:
    data['smarket']['inv'][ath]={}
    data['smarket']['inv'][ath]['sun']=0
    data['smarket']['inv'][ath]['smirk']=0
    data['smarket']['inv'][ath]['smile']=0
    data['smarket']['inv'][ath]['joy']=0
    data['smarket']['inv'][ath]['pens']=0
  if thing == "😎" or thing ==1:
    cost=data['smarket']['stocks']['sun']*num
    if data['money'][ath]<cost:
      await ctx.send("You cannot afford this")
    elif (data['smarket']['inv'][ath]['sun'] + num)>25:
      await ctx.send("You can only have 25 of one type in your inventory.")
    else:
      data['money'][ath]-=cost
      data['smarket']['inv'][ath]['sun']+=num
      data['smarket']['trades']['sun']+=num
      await ctx.send("Transaction complete, it cost you {}. Check your inventory.".format(cost))
  elif thing == "😏" or thing ==2:
    cost=data['smarket']['stocks']['smirk']*num
    if data['money'][ath]<cost:
      await ctx.send("You cannot afford this")
    elif (data['smarket']['inv'][ath]['smirk'] + num)>25:
      await ctx.send("You can only have 25 of one type in your inventory.")
    else:
      data['money'][ath]-=cost
      data['smarket']['inv'][ath]['smirk']+=num
      data['smarket']['trades']['smirk']+=num
      await ctx.send("Transaction complete, it cost you {}. Check your inventory.".format(cost))
  elif thing == "😃" or thing ==3:
    cost=data['smarket']['stocks']['smile']*num
    if data['money'][ath]<cost:
      await ctx.send("You cannot afford this")
    elif (data['smarket']['inv'][ath]['smile'] + num)>25:
      await ctx.send("You can only have 25 of one type in your inventory.")
    else:
      data['money'][ath]-=cost
      data['smarket']['inv'][ath]['smile']+=num
      data['smarket']['trades']['smile']+=num
      await ctx.send("Transaction complete, it cost you {}. Check your inventory.".format(cost))
  elif thing == "😂" or thing ==4:
    cost=data['smarket']['stocks']['joy']*num
    if data['money'][ath]<cost:
      await ctx.send("You cannot afford this")
    elif (data['smarket']['inv'][ath]['joy'] + num)>25:
      await ctx.send("You can only have 25 of one type in your inventory.")
    else:
      data['money'][ath]-=cost
      data['smarket']['inv'][ath]['joy']+=num
      data['smarket']['trades']['joy']+=num
      await ctx.send("Transaction complete, it cost you {}. Check your inventory.".format(cost))
  elif thing == "😔" or thing ==5:
    cost=data['smarket']['stocks']['pens']*num
    if data['money'][ath]<cost:
      await ctx.send("You cannot afford this")
    elif (data['smarket']['inv'][ath]['pens'] + num)>25:
      await ctx.send("You can only have 25 of one type in your inventory.")
    else:
      data['money'][ath]-=cost
      data['smarket']['inv'][ath]['pens']+=num
      data['smarket']['trades']['pens']+=num
      await ctx.send("Transaction complete, it cost you {}. Check your inventory.".format(cost))
  else:
    await ctx.send("Invalid stock id.")
  dump()

@bot.command(aliases=["se"])
@commands.has_role("Alive")
async def sell(ctx,thing,num:int=1):
  '''Use this to sell stocks.'''
  if int(gamestate)!=3:
    await ctx.send("There is no game going on right now.")
    return
  if data['smarket']['state']==0:
    await ctx.send("Market is closed.")
    return
  if num<0:
    await ctx.send("Number cannot be nagative.")
    return
  ath=str(ctx.author.id)
  if ath not in data['smarket']['inv']:
    data['smarket']['inv'][ath]={}
    data['smarket']['inv'][ath]['sun']=0
    data['smarket']['inv'][ath]['smirk']=0
    data['smarket']['inv'][ath]['smile']=0
    data['smarket']['inv'][ath]['joy']=0
    data['smarket']['inv'][ath]['pens']=0
  if thing == "😎" or thing ==1:
    cost=data['smarket']['stocks']['sun']*num
    if (data['smarket']['inv'][ath]['sun'] - num)<0:
      await ctx.send("You canonly sell what yuou have.")
    else:
      data['money'][ath]+=cost
      data['smarket']['inv'][ath]['sun']-=num
      data['smarket']['trades']['sun']-=num
      await ctx.send("Transaction complete, you earned {}. Check your inventory.".format(cost))
  elif thing == "😏" or thing ==2:
    cost=data['smarket']['stocks']['smirk']*num
    if (data['smarket']['inv'][ath]['smirk'] - num)<0:
      await ctx.send("You canonly sell what yuou have.")
    else:
      data['money'][ath]+=cost
      data['smarket']['inv'][ath]['smirk']-=num
      data['smarket']['trades']['smirk']-=num
      await ctx.send("Transaction complete, you earned {}. Check your inventory.".format(cost))
  elif thing == "😃" or thing ==3:
    cost=data['smarket']['stocks']['smile']*num
    if (data['smarket']['inv'][ath]['smile'] - num)<0:
      await ctx.send("You canonly sell what yuou have.")
    else:
      data['money'][ath]+=cost
      data['smarket']['inv'][ath]['smile']-=num
      data['smarket']['trades']['smile']-=num
      await ctx.send("Transaction complete, you earned {}. Check your inventory.".format(cost))
  elif thing == "😂" or thing ==4:
    cost=data['smarket']['stocks']['joy']*num
    if (data['smarket']['inv'][ath]['joy'] - num)<0:
      await ctx.send("You canonly sell what yuou have.")
    else:
      data['money'][ath]+=cost
      data['smarket']['inv'][ath]['joy']-=num
      data['smarket']['trades']['joy']-=num
      await ctx.send("Transaction complete, you earned {}. Check your inventory.".format(cost))
  elif thing == "😔" or thing ==5:
    cost=data['smarket']['stocks']['pens']*num
    if (data['smarket']['inv'][ath]['pens'] - num)<0:
      await ctx.send("You canonly sell what yuou have.")
    else:
      data['money'][ath]+=cost
      data['smarket']['inv'][ath]['pens']-=num
      data['smarket']['trades']['pens']-=num
      await ctx.send("Transaction complete, you earned {}. Check your inventory.".format(cost))
  else:
    await ctx.send("Invalid stock id.")
  dump()

@bot.command(aliases=["pri"])
@commands.has_role("Alive")
async def price(ctx):
  '''Use this to see the price of all stocks.'''
  if data['smarket']['state']==0:
    await ctx.send("The market it closed right now.")
  a=data['smarket']['stocks']['sun']
  b=data['smarket']['stocks']['smirk']
  c=data['smarket']['stocks']['smile']
  d=data['smarket']['stocks']['joy']
  e=data['smarket']['stocks']['pens']
  await ctx.send("Cost of :sunglasses: is {} \nCost of :smirk: is {} \nCost of :smiley: is {} \nCost of :joy: is {} \nCost of :pensive: is {} \n".format(a,b,c,d,e))



@bot.command(aliases=["r"])
async def role(ctx,*,role):
    '''Returns role info. '''
    await rolehelp(role,ctx)

async def rolehelp(role,chnl):
    if role == "king" or role == "1":
          await chnl.send("```1. King - \n -Doesn't have any power but faction can't respawn with out him ! Kill this person to destroy the faction! \n -Can't respawn.```")
    elif role == "warrior" or role =="2":
        await chnl.send("```2.Warrior - \n -Doesn't have any powers. \n -Respawns in 1 in game days.```")
    elif role == "potion master" or role =="3" :
        await chnl.send("```3.Potion master - \n -Can choose to craft a poison potion (2 days preparation time) which can kill 2 people at once, a protection potion (2 days preparation time) which can be used to protect someone once for 1 attack, or a respawn potion (2 days preparation time) which can used to respawn a person instantly (except the king) and use it on someone or store it for future use. \n -The potion master cannot make multiple potions at once. And potions are not immediate. \n - If a potion master is killed , they will lose all potions stored , and will lose progress on any potion they were crafting. \n -Potion making starts as soon as sun sets and will end a few days later when the sun sets and can be used as soon as it's done. Kill potions acts at night end. Respawn and protection potion are instant. \n -Respawns in 3 days.```")
    elif role == "finisher" or role =="4" :
        await chnl.send("```4.Finisher - \n  -Can delay a person's respawn by 2 day. \n   - Action is instant. Respawns in 3 days.```")
    elif role == "chief warrior" or role =="5" :
        await chnl.send("```5.Chief Warrior - \n -Chooses who to kill and takes advice from other members of the faction,respawns much quicker at the start and then it  get slower. \n - Respawns in 1 day on the first death , then 2 days after.```")
    elif role == "prince" or role =="6" :
        await chnl.send("```6.Prince - \n  -Takes the place of the king , if he is alive when the king dies. \n - Respawns in a day as prince , but can't respawn as the king.```")
    elif role == "disabler" or role =="7" :
        await chnl.send("```7.Disabler - \n  -Can immobilize a person for a day, making him unable to use any powers. \n -Respawns in 3 days.```")
    elif role == "killer" or role =="8" :
        await chnl.send("```8.Killer - SOLO role \n - Is a solo role , he kills people individually once a day. Wins if he has killed at least 50% of the people in game at least once. \n  -Can't respawn```")
    elif role == "wizard" or role =="9" :
        await chnl.send("```9.Wizard - \n  - Can reduce a player's respawn time by 1 day or increase someone's respawn time by 1 day. \n  - Action is instant. Respawns in 3 days.```")
    elif role == "camo warrior" or role =="10" :
        await chnl.send("```10.Camo warrior - \n  -This role cannot be killed when he activates camo mode. Cooldown for this ability is 1 days. \n -Respawns in 2 days.```")
    elif role == "seer" or role =="11" :
        await chnl.send("```11. Seer - \n -Can get the role of a person, by using his ability on a person a certain number of times. (y=30/x , rounded up, where y is number of checks and x is people playing.). \n -Doesn't lose progress if killed or changes target in between. \n -Gets answers as soon as they check y number of times. Respawns in 3 days.```")
    elif role == "guard" or role =="12" :
        await chnl.send("```12.Guard - \n   - Can protect someone once every lifetime.(He will die instead of the person he protects.) Cannot change target after initially picking it. \n - Respawns in 2 days.```")
    elif role == "observer" or role =="13" :
        await chnl.send("```13.Observer - \n -Can know the color of a targeted person instantly. \n -Respawns in 2 days.```")
    elif role == "painter" or role =="14" :
        await chnl.send("```14. Painter - \n  -Can paint a person to make his allegiance appear as something else to checks. \n -Respawns in 2 days.```")
    elif role == "builder" or role =="15" :
        await chnl.send("```15.Builder - \n - Building materials will be awarded to the builder when any opponent dies. Each person killed by his team gives him 2 pieces ,  any non team kills from outside the team gives him 1 piece. \n -The Builder can build a wall with 12 pieces which stops all attacks for 1 night, A fort for 16 pieces which stops all attacks for 2 nights or a trench with 20 parts which kills the first 2 people to attack their team.  Any kills using the trench do not award parts. \n -They can earn parts while dead but can only build when alive. Any structure built lasts as long as it doesn't get destroyed. \n -Respawns in 3 day.```")
    elif role == "double agent" or role =="16" :
        await chnl.send("```16.Double agent - SOLO role - \n - Appears like a warrior to any two factions. He can switch to any one fraction in the game and at that point turns into an regular warrior .If he doesn't switch fast enough , and he gets killed , he cannot respawn  and will lose.```")
    elif role == "strong warrior" or role =="17" :
        await chnl.send("```17.Strong Warrior- \n -Needs to be attacked twice for him to die. He does not lose this ability after dying. \n   -Respawns in 3 days.```")
    elif role == "ex warrior" or role =="18" :
        await chnl.send("```18.Ex Warrior- \n -Is allowed to kill 1 person during the game at any time. (Not an immediate action. \n -Respawns in 1 days```")
    elif role == "priest" or role =="19" :
        await chnl.send("```19.Priest- \n  - Can pray for someone (even for people outside their team) every day. Once he has prayed for someone thrice , they will be protected from the next attack. \n   -Respawns in 3 days.```")
    elif role == "curse caster" or role =="20" :
        await chnl.send("```20.Curse caster- \n   -Can reset the priest's progress of prayers on someone. If someone has a complete protecting , cursing on him twice will remove the protection. Can cast a curse everyday. \n  - Curse casting is immediate. Respawns in 2 days.```")
    elif role == "kidnapper" or role =="21" :
        await chnl.send("```21.Kidnapper - SOLO role - \n  -Can kidnap a person once every 3 days , after night 1. \n  -Kidnapped people lose access to their chats and loses the ability to perform actions. The kidnapped person also cannot be killed during this duration. The kidnapper gets all the money that the kidnapped person had. The kidnapper is kept anonymous and can send  anonymous messages to the kidnapped person. The team can free the kidnapped person after paying a ransom of 1000c. \n   -Kidnapper cannot respawn. If the kidnapper is killed , then all kidnapped people are released. \n  -The kidnapper wins when he has kidnapped all the kings atleast once. \n -Kidnapping gets done when day starts.```")
    elif role == "item agent" or role =="22" :
        await chnl.send("```22.Item Agent - SOLO role - \n -Every night he can contact a person and he gives him a choice. \n  -The contacted person can choose to kill a person or to reveal a person's role and color. ( or to ignore him) \n -If the contacted person accepts, The agent will take all his money. \n  -If the Item agent gets 2500c (By trades only.) , he wins. \n -If a person contacted has less than 200c , he will automatically die. \n -The person gets contacted as day begins.```")
    elif role == "life transferrer" or role =="23" :
        await chnl.send("```23.Life transferrer- \n  -Can make it so that his life is transferred to another person in game. Doing so will cause all attacks towards them to fail , but if their target is attacked , they will die. \n    -  Life will be transferred instantly. Respawns in 3 days.```")
    elif role == "role stealer" or role =="24" :
        await chnl.send("```24.Role stealer- \n    -Can steal the ability of a dead person. Stolen person will be able to use ability as well. Cannot steal from teammates.\n -The role stealer will know the stolen role immediately but cannot use it's powers till the next night. \n -Respawns in 3 days.```")
    elif role == "death swapper" or role =="25" :
        await chnl.send("```25.Death Swapper- \n -Can make anyone respawn for the cost of killing himself. (Person respawns the next day) \n -Swapping is INSTANT .Respawns in 2 days```")
    elif role == "gem trader" or role =="26" :
        await chnl.send("```26.Gem trader - SOLO role \n - Starts off the game with a certain number of gems. (Number of gems = Number of people/4 , Rounded down) Can give a gem to a person every night. If a person with a gem is attacked , the attack is cancelled and the gem is automatically given to the attacker. \n -Anyone with a gem can pass it to others. \n -If the gem trader survives 1 full day with 0 gems , they win. Anyone with a gem the night prior to the gem trader winning , will die. These deaths are counted as NIGHT KILLS and not day kills. Any form of night protection will save you from this. (Even a guard protection.) \n -Gems cannot be given to anyone with a gem (Except the gem trader). Holding a gem disables you from performing any actions. \n -If you are killed by the daily tribute while holding a gem , you will be killed and the gem will be returned to the gem trader. \n -The gem trader can also get rid of one of his gems by paying 5000c. \n -Gems will be given after kills.```")
    elif role == "disguiser" or role =="27":
        await chnl.send("```27. Disguiser - \n -Can make any person appear as any other role to all checks. \n - Power is instant. Respawns in 2 days.```")
    elif role == "alert warrior" or role=="28":
        await chnl.send("```28. Alert Warrior - \n -Can choose to stay awake at night , killing anyone who visits him. Cooldown for his ability is 2 days. \n -Action is instant. Respawns in 2 days.```")
    elif role == "assassin" or role=="29":
        await chnl.send("```29. Assassin- \n -Can kill one every night. \n -Kill is night end. Respawns in 3 days.```")
    elif role == "merchant" or role=="30":
        await chnl.send("```30. Merchant- \n -Will get back 50% of any cash spent by his team for any market items. \n -Will get the cash back as soon as day ends. Respawns in 2 days.```")
    elif role== "evil prince" or role=="31":
        await chnl.send("```31.Evil Prince - SOLO - \n -Similar to a prince but isn't actually on the team. The evil prince's goal is to just get their King killed. \n -Can't respawn but wins immediately if their team king is eliminated. \n -Is disguised as a regular prince in role list and all checks.```")
    elif role== "cult leader" or role=="32":
        await chnl.send("```32.Cult Leader- SOLO - \n - Invites people to new solo team every night.(attempts to invite a King ,Prince or a solo role will fail). Winning with the solo is now the new team's goal. People need to kill everyone not on the solo team , they still respawn and also are disguised. (The Cult Leader is now their new king.)Invited person joins team when the night gets over. \n - Everyone in solo team stops respawning once leader dies. \n  -Invited people appear to still be in old team , but are actually part of the solo team.```")
    elif role== "rich person" or role=="33":
        await chnl.send("```33.Rich Person - \n -Any money used for them in tribute is counted as x2 . \n -Respawns in 1 day.```")
    elif role== "minister" or role=="34":
        await chnl.send("```34.Minister - \n -If the minister is alive when the king dies , Everyone will be able to respawn again once. \n -Respawns in 1 day.```")
    elif role== "weapon smith" or role=="35":
        await chnl.send("```35.Weapon Smith - \n -Can craft a weapon to help their team. (Can craft a sword - 2 days or a cannon - 4 days.) Loses progress if killed when crafting. \n -Can keep the weapons to use any night (If killed, their inventory will be reset.). Or they can give it to a killing role to boost the kill ability. A sword allows to kill x2 number of people and a cannon allows to kill x3 number of people. \n -A person can use only 1 weapon for 1 night. \n          -Weapon making starts as soon as sun sets and will end a few days later when the sun sets and can be used as soon as it's done. Weapons can be applied for a night instantly \n -Respawns in 3 days.```")
    elif role== "postman" or role=="36":
        await chnl.send("```36.Postman - SOLO - \n -Can choose to give their target a Death package (Die during night) or a protection package ( can't die during night.). The target isn't informed what package they receive. The target can choose to open it or dispose it. \n - If postman kills 4 people or kills 2 and saves 2 in 1 game, he wins. \n          -Package gets delivered when day starts.```")
    elif role== "healer" or role=="37":
        await chnl.send("```37.Healer - \n -Heals people to allow them to spawn faster. (Reduces time by 2 days.) \n -Respawns in 3 days.```")
    elif role== "magician" or role=="38":
        await chnl.send("```38. Magician - \n -Is allowed to submit a list of up to 3 guesses of people with their correct roles and correct teams. If all three guesses are correct , they will be informed. But even if one of the guesses is wrong , the rest will not be confirmed. \n -Action is immediate. Respawns in 3 days.```")
    elif role=="list" or role=="l":
        await chnl.send("All the available roles are- \n ``` 1.king \n 2.warrior \n 3.potion master \n 4.finisher \n 5.chief warrior \n 6.prince \n 7.disabler \n 8.killer \n 9.wizard \n 10.camo warrior \n 11.seer \n 12.guard \n 13.observer \n 14.painter \n 15.builder \n 16.double agent \n 17.strong warrior \n 18.ex warrior \n 19.priest \n 20.curse caster \n 21.kidnapper \n 22.item agent \n 23.life transferrer \n 24.role stealer \n 25.death swapper \n 26.gem trader \n 27.disguiser \n 28.alert warrior \n 29.assassin \n 30.merchant \n 31.evil prince \n 32.cult leader \n 33.rich person \n 34.minister \n 35.weapon smith \n 36.postman \n 37.healer \n 38.magician```")
    else:
        await chnl.send("Error! Role not found.Do not capitalise role names. You can also use the number (Found in #role info) to represent the role.\n All the available roles are- \n ``` 1.king \n 2.warrior \n 3.potion master \n 4.finisher \n 5.chief warrior \n 6.prince \n 7.disabler \n 8.killer \n 9.wizard \n 10.camo warrior \n 11.seer \n 12.guard \n 13.observer \n 14.painter \n 15.builder \n 16.double agent \n 17.strong warrior \n 18.ex warrior \n 19.priest \n 20.curse caster \n 21.kidnapper \n 22.item agent \n 23.life transferrer \n 24.role stealer \n 25.death swapper \n 26.gem trader \n 27.disguiser \n 28.alert warrior \n 29.assassin \n 30.merchant \n 31.evil prince \n 32.cult leader \n 33.rich person \n 34.minister \n 35.weapon smith \n 36.postman \n 37.healer \n 38.magician```")

async def change():
  global data
  if data['smarket']['trades']['sun']>20:
    data['smarket']['stocks']['sun']+=25
    data['smarket']['trades']['sun']=0
  elif data['smarket']['trades']['sun']<0:
    data['smarket']['stocks']['sun']-=25
    data['smarket']['trades']['sun']=0
    if data['smarket']['stocks']['sun']<=0:
      data['smarket']['stocks']['sun']=25
  else:
    mylist=[25,0,-25]
    data['smarket']['stocks']['sun']+=random.choice(mylist)
    if data['smarket']['stocks']['sun']<=0:
      data['smarket']['stocks']['sun']=25

  if data['smarket']['trades']['smirk']>20:
    data['smarket']['stocks']['smirk']+=20
    data['smarket']['trades']['smirk']=0
  elif data['smarket']['trades']['smirk']<0:
    data['smarket']['stocks']['smirk']-=20
    data['smarket']['trades']['smirk']=0
    if data['smarket']['stocks']['smirk']<=0:
      data['smarket']['stocks']['smirk']=20
  else:
    mylist=[20,0,-20]
    data['smarket']['stocks']['smirk']+=random.choice(mylist)
    if data['smarket']['stocks']['smirk']<=0:
      data['smarket']['stocks']['smirk']=20

  if data['smarket']['trades']['smile']>0:
    data['smarket']['stocks']['smile']+=5
    data['smarket']['trades']['smile']=0
  elif data['smarket']['trades']['smile']<0:
    data['smarket']['stocks']['smile']-=5
    data['smarket']['trades']['smile']=0
    if data['smarket']['stocks']['smile']<=0:
      data['smarket']['stocks']['smile']=5
  else:
    mylist=[5,0,-5]
    data['smarket']['stocks']['smile']+=random.choice(mylist)
    if data['smarket']['stocks']['smile']<=0:
      data['smarket']['stocks']['smile']=5

  if data['smarket']['trades']['joy']>0:
    data['smarket']['stocks']['joy']+=5
    data['smarket']['trades']['joy']=0
  elif data['smarket']['trades']['joy']<0:
    data['smarket']['stocks']['joy']-=5
    data['smarket']['trades']['joy']=0
    if data['smarket']['stocks']['joy']<=0:
      data['smarket']['stocks']['joy']=5 
  else:
    mylist=[5,0,-5]
    data['smarket']['stocks']['joy']+=random.choice(mylist)
    if data['smarket']['stocks']['joy']<=0:
      data['smarket']['stocks']['joy']=5

  if data['smarket']['trades']['pens']>15:
    data['smarket']['stocks']['pens']+=5
    data['smarket']['trades']['pens']=0
  elif data['smarket']['trades']['pens']<5:
    data['smarket']['stocks']['pens']-=5
    data['smarket']['trades']['pens']=0
    if data['smarket']['stocks']['pens']<=0:
      data['smarket']['stocks']['pens']=5
  else:
    mylist=[5,0,-5]
    data['smarket']['stocks']['pens']+=random.choice(mylist)
    if data['smarket']['stocks']['pens']<=0:
      data['smarket']['stocks']['pens']=5
  dump()



async def score(ath,msg):
    global data
    global earnd
    global lstmsg
    if not ath in data['money']: 
      if ath not in data['players']:
        return
      else:
            data['money'][ath]=0
            dump()
            #print(data[ath])
    else:
          coins=[10,20]
          dcoins=[5,10]
          
          if not ath in earnd:
            if not str(ath) in lstmsg:
              lstmsg[str(ath)]=" "
            if lstmsg[str(ath)]==msg:
              return
            else:
              try:

                if data['players'][ath]['state'] ==0:
                    add= random.choice(dcoins)
                    data['money'][ath]+=int(add)
                    earnd.append(ath)
                    lstmsg[str(ath)]=msg
                else:
                  add= random.choice(coins)
                  data['money'][ath]+=int(add)
                  earnd.append(ath)
                  lstmsg[str(ath)]=msg
              except KeyError:
                add= random.choice(coins)
                data['money'][ath]+=int(add)
                earnd.append(ath)
                lstmsg[str(ath)]=msg
          else:
            return
          dump()
          #print(data[ath])
            
def dump():
    my_collection = db.main
    my_collection.drop()
    my_collection.insert_one(data)
    '''with open('data.json', 'w+') as f:
        json.dump(data, f)'''
keep_alive.keep_alive()
bot.run(token)
