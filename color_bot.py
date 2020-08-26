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
from cogs.roleinfo import rolehelp
#from loaddump import load,dump,data,gamestate
import loaddump

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
      await load(bot)
      await asyncio.sleep(5)
      if int(loaddump.gamestate)==1:
          await bot.change_presence(activity=discord.Game(name="Signups open!", type=1))
      elif int(loaddump.gamestate)==2:
          await bot.change_presence(activity=discord.Game(name="Signups are closed.A game will soon begin.", type=1))
      elif int(loaddump.gamestate)==3:
          await bot.change_presence(activity=discord.Game(name="Game running.", type=1))
      elif int(loaddump.gamestate)==4:
          await bot.change_presence(activity=discord.Game(name="Game concluded!", type=1))
      else:
          await bot.change_presence(activity=discord.Game(name=" Colour battles!", type=1))
      print("Working boi!")
      await loaddump.spamchannel.send("The bot is online!")
      


#admin/informer

   
     

#moderator/helper
       
@bot.command(aliases=["a"])
@commands.has_role("Helpers")
async def listallr(ctx):
    '''Lists everyone's roles. <Helpers>'''
    await load()
    temp = ""
    for user in loaddump.data['players']:
        guildd=bot.get_guild(448888674944548874)
        userr=discord.utils.get(guildd.members,id=int(user))
        temp +="{} has the role `{}` \n".format(userr.mention,loaddump.data['players'][user]['role'])
    msg = await ctx.send("Loading.")
    await msg.edit(content=temp)


@bot.command(aliases=["ar"])
@commands.has_role("Helpers")
async def addrole(ctx,role,team,litrole):
    '''Adds roles to the role list.(Similar roles must be entered with a number after them , teams can only be red , blue , green or yellow.(No Caps) Any other team will be considered as a solo team) <Helpers>'''
    await load()
    if (int(loaddump.gamestate) >= 3):
        await ctx.send("A game is already going on.")
        return
    loaddump.data['roles'].append(role)
    loaddump.data['rt'][role]={}
    loaddump.data['rt'][role]['team']=team
    loaddump.data['rt'][role]['lirole'] = litrole
    await ctx.send("{} added for the team {}.".format(role,team))
    dump()
    
@bot.command(aliases=["rr"])
@commands.has_role("Helpers")
async def removerole(ctx,role,team):
    '''Removes a role from the role list. <Helpers>'''
    await load()
    if (int(loaddump.gamestate) >= 3):
        await ctx.send("A game is already going on.")
        return
    loaddump.data['roles'].remove(role)
    #loaddump.data['rt'].remove(role)
    del loaddump.data['rt'][role]
    await ctx.send("{} removed.".format(role))
    dump()
   
@bot.command(aliases=["lr"])
@commands.has_role("Helpers")
async def listroles(ctx):
    '''Prints the entire role list. <Helpers>'''
    await load()
    temp = ""
    await ctx.send("The rolelist is - ")
    for role in loaddump.data['roles']:
        temp +="{} of {}\n".format(role,loaddump.data['rt'][role])
    msg = await ctx.send("Loading.")
    await msg.edit(content=temp)
    
@bot.command(aliases=["cr"])
@commands.has_role("Helpers")
async def clearroles(ctx):
    '''Removes all roles from the list. <Helpers>'''
    await load()
    if (int(loaddump.gamestate) >= 3):
        await ctx.send("A game is already going on.")
        return
    loaddump.data['roles']=[]
    loaddump.data['rt']={}
    await ctx.send("Cleared.")
    dump()

@bot.command(aliases=["eg"])
@commands.has_role("Helpers")
async def endgame(ctx):
    '''Ends the game. <Helpers>'''
    await load()
    global gamestate
    if int(loaddump.gamestate)!=3:
        await ctx.send("A game isn't even going on.")
        return
    loaddump.gamestate=4
    loaddump.data['gamastate']=4
    await bot.change_presence(activity=discord.Game(name="Game concluded!", type=1))
    for user in loaddump.data['players']:
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
    await load()
    if int(loaddump.gamestate)!=3:
        await ctx.send("There isn't a game going on.")
        return
    loaddump.data['players'][str(user.id)]['state']=0
    guildd=bot.get_guild(448888674944548874)
    role = discord.utils.get(guildd.roles, name="Respawning")
    await user.add_roles(role)
    role = discord.utils.get(guildd.roles, name="Players")
    await user.remove_roles(role)
    for cc in loaddump.data['players'][str(user.id)]['incc']:
        chnl = bot.get_channel(int(cc))
        await chnl.set_permissions(user, read_messages=True,send_messages=False,add_reactions=False)
    await ctx.send("Killed {}.".format(user.mention))
    dump()
    
@bot.command(aliases=["r"])
@commands.has_role("Helpers")
async def respawn(ctx,user:discord.Member):
    '''Respawns a person in game <Helpers>'''
    await load()
    if int(loaddump.gamestate)!=3:
        await ctx.send("There isn't a game going on.")
        return
    loaddump.data['players'][str(user.id)]['state']=1
    guildd=bot.get_guild(448888674944548874)
    role = discord.utils.get(guildd.roles, name="Respawning")
    await user.remove_roles(role)
    role = discord.utils.get(guildd.roles, name="Players")
    await user.add_roles(role)
    for cc in loaddump.data['players'][str(user.id)]['incc']:
        chnl = bot.get_channel(int(cc))
        await chnl.set_permissions(user, read_messages=True,send_messages=True,add_reactions=True)
    await ctx.send("Respawned {}.".format(user.mention))
    dump()

@bot.command(aliases=["pk"])
@commands.has_role("Helpers")
async def pkill(ctx,user:discord.Member):
    '''Kills a person permanently in game. <Helpers>'''
    await load()
    if int(loaddump.gamestate)!=3:
        await ctx.send("There isn't a game going on.")
        return
    loaddump.data['players'][str(user.id)]['state']=0
    guildd=bot.get_guild(448888674944548874)
    role = discord.utils.get(guildd.roles, name="Respawning")
    await user.remove_roles(role)
    role = discord.utils.get(guildd.roles, name="Players")
    await user.remove_roles(role)
    role = discord.utils.get(guildd.roles, name="Dead")
    await user.add_roles(role)
    for cc in loaddump.data['players'][str(user.id)]['incc']:
        chnl = bot.get_channel(int(cc))
        await chnl.set_permissions(user, read_messages=True,send_messages=False,add_reactions=False)
    await ctx.send("Permanently killed {}.".format(user.mention))
    dump()


@bot.command(aliases=["mg"])
@commands.has_role("Helpers")
async def massgive(ctx,cash):
  '''Gives a certain amount of cash to everyone who has an account. <Helpers>'''
  await load()
  if (int(loaddump.gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  for  ath in loaddump.data['money']:
    loaddump.data['money'][ath]+=int(cash)
  await ctx.send("Added {} to everyone who had an account.".format(cash))
  dump()

@bot.command(aliases=["mbal"])
@commands.has_role("Helpers")
async def masterbalance(ctx,member:discord.Member):
  '''Allows to see the balance of another player <Helpers>'''
  await load()
  if (int(loaddump.gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  id=str(member.id)
  await ctx.send("{}'s balance is {}.".format(member.mention,loaddump.data['money'][id]))

@bot.command(aliases=["ca"])
@commands.has_role("Helpers")
async def createauction(ctx,name,*,text):
    '''Allows the user to create a auction <Helpers>'''
    await load()
    if (int(loaddump.gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    global data
    guildd=bot.get_guild(448888674944548874)
    mark=discord.utils.get(guildd.channels,name="market")
    loaddump.data['auction']['state']=1
    await mark.send("__**ITEM - {}**__".format(name))
    await mark.send("Perks - {}".format(text))
    aucmsg = await mark.send("Current bid - ")
    loaddump.data['auction']['msg']=str(aucmsg.id)
    loaddump.data['auction']['chn']=str(aucmsg.channel.id)
    loaddump.data['auction']['bid']=0
    loaddump.data['auction']['bider']=""
    dump()

@bot.command(aliases=["cla"])
@commands.has_role("Helpers")
async def closeauction(ctx):
  '''Allows the user to close a auction <Helpers>'''
  await load()
  if (int(loaddump.gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  global data
  if loaddump.data['auction']['state']==0:
    await ctx.send("There is no auction going on right now.")
    return
  loaddump.data['auction']['state']=0
  who=loaddump.data['auction']['bider']
  cost=loaddump.data['auction']['bid']
  await ctx.send("Congrats! {} has won the item auctioned for about {} ! ".format(who,cost))
  loaddump.data['auction']['msg']=""
  loaddump.data['auction']['chn']=""
  loaddump.data['auction']['bid']=0
  loaddump.data['auction']['bider']=""
  dump()


#all
@bot.command()
async def ping(ctx):
    '''Returns Pong.'''
    await load()
    print("Pong!")
    await ctx.send("Pong!")
    dump()
    
@bot.command(aliases=["j","join"])
async def signup(ctx):
    '''Allows you to signup for a game.Sign out by typing the command again.'''
    await load()
    global data
    if (int(loaddump.gamestate) != 1):
        await ctx.send("Sign ups are closed right now. Try joining when they are open , of after the game has concluded. Contact a Informer or a helper if you need help.")
        return
    ath=str(ctx.author.id) 
    if not ath in loaddump.data['signedup']:
      if not ath in loaddump.data['specters']:
        loaddump.data['signedup'][ath] = 1
        guildd=bot.get_guild(448888674944548874)
        role = discord.utils.get(guildd.roles, name="Signed-Up!")
        await ctx.send("You have been signed-up! :thumbsup:")
        await ctx.author.add_roles(role)
        dump()
      else:
        await ctx.send("You are currently spectating. Kindly stop spectating if you want to play.")
    else:
        loaddump.data['signedup'].pop(ath)
        guildd=bot.get_guild(448888674944548874)
        role = discord.utils.get(guildd.roles, name="Signed-Up!")
        await ctx.send("You have been signed-out!")
        await ctx.author.remove_roles(role)
        dump()
    
@bot.command(aliases=["sl"])
async def slist(ctx):
    '''Shows a list of everyone signed up.'''
    await load()
    temp = ""
    tempno=0
    temp+="The list of people signed-up is - \n"
    for member in loaddump.data['signedup']:
        tempno+=1
        temp +="<@{}> \n".format(member)
    temp += "The number of people signed up is {} \n".format(tempno)
    msg = await ctx.send("Loading.")
    await msg.edit(content=temp)
    
@bot.command(aliases=["sp","spec"])
async def spectate(ctx):
    '''Allows you to spectate the game.'''
    await load()
    global data
    if int(loaddump.gamestate)==0:
        await ctx.send("You cannot use this command right now.")
        return
    guildd=bot.get_guild(448888674944548874)
    role = discord.utils.get(guildd.roles, name="Spectator")
    ath = str(ctx.author.id)
    if not ath in loaddump.data['specters']:
      if not ath in loaddump.data['signedup']:
        await ctx.author.add_roles(role)
        loaddump.data['specters'].append(ath)
        await ctx.send("You are now spectating! ")
      else:
        await ctx.send("You have signed up for a game. Please sign out before spectating.")
    else:
      await ctx.author.remove_roles(role)
      loaddump.data['specters'].remove(ath)
      await ctx.send("You are no longer spectating! ")
    dump()
    
@bot.command(aliases=["c"])
async def bal(ctx):
    '''Prints your balance.'''
    await load()
    if (int(loaddump.gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    await ctx.send("{}'s bank balance is {}".format(ctx.author.mention,loaddump.data['money'][str(ctx.author.id)]))
    await load()
   
@bot.command(aliases=["ghs"])
@commands.has_role("Respawning")
async def ghostsay(ctx,*,msg):
    '''Use to send messages into town hall as a ghost <Respawning>'''
    await load()
    guildd=bot.get_guild(448888674944548874)
    townc=discord.utils.get(guildd.channels,name="townhall")
    taboo = "@everyone"
    if taboo in str(msg):
      await ctx.send("Please don't ping @ everyone.")
    else:
      await townc.send("<Ghost> {}".format(msg))
    '''ghosthook = Webhook('https://discordapp.com/api/webhooks/723763897764675616/9c5GmG9WKemUjWv4cEMGVfHrjjmExGvV36JmS38Hep5KqK4nOKYfayzr6OTIQa2rgZ_O')
    ghosthook.send(msg)'''
   
@bot.command(aliases=["cc"])
@commands.has_role("Players")
async def createchannel(ctx,ccname,member:discord.Member):
    '''Used to create a communication channel.'''
    await load()
    if (int(loaddump.gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    global data
    guildd=ctx.message.guild
    if int(loaddump.gamestate)!=3:
        await ctx.send("There isn't a game going on.")
        return
    if loaddump.data['money'][str(ctx.author.id)] <50:
        await ctx.send("You cannot afford to make a cc....")
        await ctx.message.delete()
        return
    if loaddump.data['code']['ccno'] ==0:
      name=loaddump.data['code']['gamecode'] +' cc1'
      await guildd.create_category(name)
    elif loaddump.data['code']['ccno']==50:
      name=loaddump.data['code']['gamecode'] +' cc2'
      await guildd.create_category(name)
    elif loaddump.data['code']['ccno']==100:
      name=loaddump.data['code']['gamecode'] +' cc3'
      await guildd.create_category(name)
    elif loaddump.data['code']['ccno']==150:
      name=loaddump.data['code']['gamecode'] +' cc4'
      await guildd.create_category(name)
    elif loaddump.data['code']['ccno']==200:
      name=loaddump.data['code']['gamecode'] +' cc5'
      await guildd.create_category(name)
    loaddump.data['money'][str(ctx.author.id)] -= 50
    author = ctx.message.author
    role0 = discord.utils.get(guildd.roles, name="Helpers")
    '''role1 = discord.utils.get(guildd.roles, name="Players")
    role2= discord.utils.get(guildd.roles, name="Spectatators")'''
    role3 = discord.utils.get(guildd.roles, name="Dead")
    role4 = discord.utils.get(guildd.roles, name="Spectator")
    overwrites = {
    guildd.default_role: discord.PermissionOverwrite(read_messages=False),
    guildd.me: discord.PermissionOverwrite(read_messages=True),
    author:discord.PermissionOverwrite(read_messages=True,add_reactions=True),
    member:discord.PermissionOverwrite(read_messages=True,add_reactions=True),
    role0:discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role3:discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role4:discord.PermissionOverwrite(read_messages=True,send_messages=False)
                 }
    if loaddump.data['code']['ccno']<50:
      name=loaddump.data['code']['gamecode'] +' cc1'
      cate = discord.utils.get(ctx.message.guild.categories, name=name)
    elif loaddump.data['code']['ccno']<100:
      name=loaddump.data['code']['gamecode'] +' cc2'
      cate = discord.utils.get(ctx.message.guild.categories, name=name)
    elif loaddump.data['code']['ccno']<150:
      name=loaddump.data['code']['gamecode'] +' cc3'
      cate = discord.utils.get(ctx.message.guild.categories, name=name)
    elif loaddump.data['code']['ccno']<200:
      name=loaddump.data['code']['gamecode'] +' cc4'
      cate = discord.utils.get(ctx.message.guild.categories, name=name)
    elif loaddump.data['code']['ccno']<250:
      name=loaddump.data['code']['gamecode'] +' cc5'
      cate = discord.utils.get(ctx.message.guild.categories, name=name)
    loaddump.data['code']['ccno']+=1
    a = await guildd.create_text_channel(str(ccname),overwrites=overwrites,category=cate)
    print(a.id)
    await a.send("This is a new cc made by {} :- \n Participants:- \n {} \n {}".format(author.mention,author.mention,member.mention))
    loaddump.data['chnls'][str(a.id)]={}
    loaddump.data['chnls'][str(a.id)]['owner']=ctx.author.id
    loaddump.data['players'][str(ctx.author.id)]['incc'].append(a.id)
    loaddump.data['players'][str(member.id)]['incc'].append(a.id)
    await ctx.message.delete()
    dump()

@bot.command(aliases=["add"])
@commands.has_role("Players")
async def addinchannel(ctx,member:discord.Member):
    '''Adds a person to the channel'''
    await load()
    if (int(loaddump.gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    chnl = ctx.channel.id
    if loaddump.data['chnls'][str(chnl)]['owner'] == ctx.author.id:
        await ctx.channel.set_permissions(member, read_messages=True,send_messages=True)
        loaddump.data['players'][str(member.id)]['incc'].append(chnl)
        await ctx.send("Welcome , {} !".format(member.mention))
    else:
        await ctx.send("You probably aren't the owner of this cc.")
    dump()
        
@bot.command(aliases=["remove"])
@commands.has_role("Players")
async def removeinchannel(ctx,member:discord.Member):
    '''Removes a person from the channel'''
    await load()
    if (int(loaddump.gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    chnl = ctx.channel.id
    if loaddump.data['chnls'][str(chnl)]['owner'] == ctx.author.id:
        await ctx.channel.set_permissions(member, read_messages=False,send_messages=False)
        loaddump.data['players'][str(member.id)]['incc'].remove(chnl)
        await ctx.send("Removed {} from the cc.".format(member.mention))
    else:
        await ctx.send("You probably aren't the owner of this cc.")
    dump()

@bot.command(aliases=["sm"])
@commands.has_role("Players")
async def sendmoney(ctx,member:discord.Member,cash):
  '''Allows alive players to send money to others.'''
  await load()
  ath=str(ctx.message.author.id)
  if (int(loaddump.gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  if int(cash) < 0:
    await ctx.send("You cannot send negative money.")
    return
  if loaddump.data['money'][ath] < int(cash):
    await ctx.send("You do not have that many coins in your account.")
    return
  loaddump.data['money'][ath]-=int(cash)
  per=str(member.id)
  loaddump.data['money'][per]+=int(cash)
  await ctx.send("Done. Sent {} to {} from {}'s account.".format(cash,member.mention,ctx.author.mention))
  dump()

@bot.command(aliases=["al"])
async def alivelist(ctx):
  '''Shows all alive players.'''
  await load()
  if int(loaddump.gamestate) != 3:
    await ctx.send("There is no game going on right now.")
    return
  temp = ""
  temp+="All alive players are- \n"
  al=0
  for member in loaddump.data['players']:
    if loaddump.data['players'][member]['state']==1:
      temp +="<@{}> \n".format(member)
      al+=1
  temp+="The number of alive players are- {} \n".format(al)
  msg = await ctx.send("Loading.")
  await msg.edit(content=temp)

@bot.command(aliases=["b"])
@commands.has_role("Players")
async def bid(ctx,cash:int):
  '''Allows the bid in the auction <King only>'''
  await load()
  global data
  ath=str(ctx.author.id)
  if int(loaddump.gamestate) != 3:
    await ctx.send("There is no game going on right now.")
    return
  if loaddump.data['auction']['state']==0:
    await ctx.send("There is no auction going on right now.")
    return
  role = loaddump.data['players'][ath]['role']
  rolet=loaddump.data['rt'][role]['lirole']
  '''if rolet!="king" and rolet!="prince": #fix
    await ctx.send("You are not a king. Please only use this command if your role is King.")
    return'''
  await ctx.message.delete()
  if cash>loaddump.data['money'][ath]:
    await ctx.send("You can only bid what you have.")
    return
  if cash <= loaddump.data['auction']['bid']:
    await ctx.send("The current bid is higher than what you're currently offering.")
    return
  loaddump.data['auction']['bid']=cash
  if loaddump.data['players'][ath]['team'] =="red":
    who= "Red King."
  elif loaddump.data['players'][ath]['team'] =="blue":
    who= "Blue King."
  elif loaddump.data['players'][ath]['team'] =="green":
    who= "Green King."
  elif loaddump.data['players'][ath]['team'] =="yellow":
    who= "Yellow King."
  else:
    who = "Unknown bidder"
  loaddump.data['auction']['bider']=who
  guildd=bot.get_guild(448888674944548874)
  channel=bot.get_channel(int(loaddump.data['auction']['chn']))
  msgid = int(loaddump.data['auction']['msg'])
  msg = await channel.fetch_message(msgid)
  await msg.edit(content="Current bid - {} by {}".format(cash,who))
  dump()

'''@bot.group()
async def info(ctx):
  pass

@info.command()
async def infoo(ctx):
  await ctx.send("Worked ig lol")'''



''''
async def load():
      #print("Working boi!")
      global data
      global annchannel
      global spamchannel
      global loaddump.gamestate
      global lstmsg
      spamchannel=bot.get_channel(450698253508542474)
      #await spamchannel.send("The bot is online!")
      lstmsg={}
      try:
          my_collection = db.main
          loaddump.data = my_collection.find_one()
          loaddump.gamestate = loaddump.data['loaddump.gamestate']''' '''
          with open('loaddump.data.json','r') as f:
              loaddump.data = json.load(f)
              print(loaddump.data)
              loaddump.gamestate = loaddump.data['loaddump.gamestate']''' '''
      except:
              print("Could not load the loaddump.data")
              loaddump.data = {}
              loaddump.data['signedup']={}
              loaddump.data['loaddump.gamestate']=0
              loaddump.gamestate=0
              loaddump.data['money']={}
              loaddump.data['roles']=[]
              loaddump.data['rt']={}
              loaddump.data['chnls']={}
              loaddump.data['specters']=[]
              loaddump.data['code']={}
              loaddump.data['auction']={}
              dump()
              await spamchannel.send("Warning! Data.json wasn't found. Please check if anything is wrong.")
                  

def dump():
    my_collection = db.main
    my_collection.drop()
    my_collection.insert_one(loaddump.data)''' '''
    with open('loaddump.data.json', 'w+') as f:
        json.dump(loaddump.data, f)'''

bot.load_extension('cogs.test')
bot.load_extension('cogs.events')
bot.load_extension('cogs.roleinfo')
bot.load_extension('cogs.informer')
bot.load_extension('cogs.helper')
bot.load_extension('cogs.gamestart')


keep_alive.keep_alive()
bot.run(token)
