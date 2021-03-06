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
import copy, inspect
from better_profanity import profanity
import textwrap
import io
import emoji as emj
import typing
import math


token = str(os.environ.get("tokeno"))
dbpass=str(os.environ.get("dbpass"))

intents = discord.Intents.default()
intents.members = True
intents.presences = True

profanity.load_censor_words(whitelist_words=['damn'])

bot = commands.Bot(command_prefix =commands.when_mentioned_or('!','$'),intents=intents)
logging.basicConfig(level=logging.INFO)



#bot.remove_command('help')

client = pymongo.MongoClient("mongodb+srv://Topkinsme:"+dbpass+"@top-cluster.x2y8s.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.cbbot

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
    global gifted
    spamchannel=bot.get_channel(450698253508542474)
    await spamchannel.send("The bot is online!")
    lstmsg={}
    try:
        my_collection = db.main
        data = my_collection.find_one()
        gamestate = data['gamestate']
        gifted=[]
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
            data['bauction']={}
            data['building']={}
            data['smarket']={}
            data['marketalert']=[]
            data['poll']={}
            data['lottery']=0
            dump()
            await spamchannel.send("Warning! Data.json wasn't found. Please check if anything is wrong.")
    if int(gamestate)==1:
        await bot.change_presence(activity=discord.Game(name="Signups open!", type=1))
    elif int(gamestate)==2:
        await bot.change_presence(activity=discord.Game(name="Signups are closed.A game will soon begin.", type=1))
    elif int(gamestate)==3:
        num = data['code']['gamephase']
        if num %2==0:
          text = f"Day {int(num/2)}"
        else:
          text = f"Night {int((num+1)/2)}"
        await bot.change_presence(activity=discord.Game(name=f"A game. It's {text} now.", type=1))
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


@tasks.loop(minutes=1)
async def my_looptwo():
    global data
    global gifted
    datee = datetime.datetime.now()
    if int(datee.strftime("%H"))%2 !=0 or (int(datee.strftime("%M"))+61)%61 !=0 :
      return 
    gifted=[]
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
      ping="NOTIFICATION! \n"
      for ath in data['marketalert']:
        ping+="<@{}>\n".format(ath)
      msg = await channel.send(ping)
      await asyncio.sleep(10)
      await msg.delete()
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
  x=bot.get_channel(750580405102706789)
  await x.edit(name="👥 Users: {}".format(a))
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
        await x.edit(name="🔰 Game ongoing. {}/{}".format(people,total)) 
  elif int(gamestate)==4:
        await x.edit(name="✅ Game concluded.")
  else:
        await x.edit(name="⏸️ No game.")
                        
@bot.event
async def on_message(message):
    global gifted
    global gamestate
    global data
    if message.author.id == 450320950026567692:
        return
    if message.guild==None:
      await spamchannel.send(f"<{message.author}> {message.content}")
    ath=str(message.author.id)
    await bot.process_commands(message)
    if int(gamestate) != 3:
        return

    if profanity.contains_profanity(message.content):
      await message.channel.send(f"Hey {message.author.mention}! Do not swear!")
      await message.delete()
      return
    user=str(message.author.id)
    try:
      data['players'][user]['msg']+=1
    except:
      pass
    ath=str(message.author.id)
    fath=message.author
    channel = message.channel
    guildd=message.guild
    await score(ath,message.content)
    if message.channel.name=="battlefield":
      n = random.randint(1,500)
      cash = random.randint(300,500)
      if n ==49:
        if message.author.id in gifted:
          return
        gifted.append(message.author.id)
        emoji = "🎁"
        await message.add_reaction(emoji)
        await message.channel.send(":tada: <@{}> has just won a prize of {}".format(ath,cash))
        try:
          data['money'][ath]+=cash
        except:
          await message.channel.send("It seems I had trouble accessing your account so I'm just going to have to keep the money with myself....")
        dump()
    elif message.channel.name=="respawning":
      n = random.randint(1,200)
      if n ==49:
        await message.channel.send("You now have the opportunity to send a gift to earth! Respond with 'bad' or 'good' depending on what you want to send! Only the first reply will be considered. If someone opens a bad package, you will get their 100c. If you send a good package and they open it, both of you get 25c.  You have 60 seconds!")
        def check(mo):
            return mo.content.lower()=='good' or mo.content.lower()=='bad' and mo.channel == message.channel
        try:
          msg = await bot.wait_for('message', timeout=60 ,check=check)
          townc=discord.utils.get(guildd.channels,name="battlefield")
          await townc.send("The dead have sent a package to you! Type 'open' to open it! You have 60 seconds!")
          def checkk(m):
              return m.content.lower()=='open' and m.channel == townc
          try:
            msgg = await bot.wait_for('message', timeout=60 ,check=checkk)
            getter=str(msgg.author.id)
            if msg.content.lower() == 'good':
                await townc.send("It was a good package, you have recieved 25c!")
                await message.channel.send("Your target opened the package, you've recieved 25 as well!")
                data['money'][getter]+=25
                data['money'][str(message.author.id)]+=25
            elif msg.content.lower() == 'bad':
                await townc.send("It was a bad package, you have lost 100c!")
                await message.channel.send("Your target opened the package, you've recieved 100!")
                data['money'][getter]-=100
                data['money'][str(message.author.id)]+=100

          except:
              await townc.send("That offer has expired!")
        except:
            await message.channel.send("That offer has expired!")
    dump()

    
@bot.event
async def on_command_error(ctx,error):
    await ctx.send(f'```py\n{error.__class__.__name__}: {error}\n```')


@bot.event
async def on_member_join(member):
    await spamchannel.send("{} joined the server".format(member.mention))
    
@bot.event
async def on_member_remove(member):
    await spamchannel.send("{} left the server".format(member.mention))
    
    if str(member.id) in data['players']:
        data['money'].pop(str(member.id))
        data['signedup'].pop(str(member.id))
        data['players'].pop(str(member.id))
    
@bot.event
async def on_message_delete(message):
    if message.author.id==450320950026567692:
      return
    await spamchannel.send("{}'s message `{}` was deleted in <#{}>".format(message.author.name,message.content,message.channel.id))
    
@bot.event
async def on_user_update(before,after):
    if before.name==after.name:
        return
    else:
        await spamchannel.send("'{}' has changed their name to '{}' .".format(before.name,after.name))

@bot.event
async def on_raw_reaction_add(payload):
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
      if int(gamestate)!=3:
        return
      await msg.remove_reaction(emoji,userr)
    elif role1 in userr.roles and emoji=="📌" and int(gamestate)==3:
      await msg.pin()
    elif emoji=="⭐":
      n=0
      for reaction in msg.reactions:
        if str(reaction)=="⭐":
          users = await reaction.users().flatten()
          n+=len(users)
      if n==4:
        chnl=bot.get_channel(749274900966932531)
        mem = discord.Embed(colour=random.randint(0, 0xffffff))
        mem.set_author(name=msg.author.name,icon_url=msg.author.avatar_url)
        if msg.content=="":
          pass
        else:
          mem.add_field(name="Message -",value=msg.content,inline="false")
        if msg.attachments==[]:
          pass
        else:
          athc=msg.attachments
          mem.set_image(url=athc[0].url)
        mem.add_field(name="Link -",value=f"[Click This!]({msg.jump_url})",inline="false")
        await chnl.send(f"<#{channelid}>",embed=mem)


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
    data['bauction']={}
    data['building']={}
    data['smarket']={}
    data['marketalert']=[]
    data['poll']={}
    data['lottery']=0
    await ctx.send("A complete erasure of all data has been done.")
    dump()
    
@bot.command()
@commands.has_role("Informer")
async def pdata(ctx):
    '''Send the complete data file. <Informer>'''
    print(data)
    await ctx.send(data)
    
@bot.command(hidden=True)
@commands.has_role("Informer")
async def sudo(ctx,who: discord.Member, *, command: str):
        """Run a command as another user optionally in another channel."""
        msg = copy.copy(ctx.message)
        channel = ctx.channel
        msg.channel = channel
        msg.author = channel.guild.get_member(who.id) or who
        msg.content = ctx.prefix + command
        new_ctx = await bot.get_context(msg, cls=type(ctx))
        #new_ctx._db = ctx._db
        await bot.invoke(new_ctx)
    
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
        '''num = data['code']['gamephase']
        if num %2==0:
          text = f"Day {int(num/2)}"
        else:
          text = f"Night {int((num+1)/2)}"'''
        text="?"
        await bot.change_presence(activity=discord.Game(name=f"A game. It's {text} now.", type=1))
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
    try:
      namee= str(data['code']['gamecode']) + ' archive'
      cate = discord.utils.get(ctx.message.guild.categories, name=namee)
      #print(cate2.channels)
      for channel in cate.channels:
          await channel.delete()
      await cate.delete()
    except:
      await ctx.send("No archives found to delete.")
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
    data['teams']=[]
    data['chnls']={}
    data['code']={}
    data['auction']={}
    data['bauction']={}
    data['building']={}
    data['smarket']={}
    data['marketalert']=[]
    data['poll']={}
    data['lottery']=0
    dump()
    await ctx.send("Reset complete!")
    dump()   
     
@bot.command(aliases=["sub"])
@commands.has_role("Informer")
async def substitute(ctx,inactivep:discord.Member,activep:discord.Member):
  '''Use this command to sub people in the game. <Informer>'''
  global data
  if (int(gamestate) != 3):
      await ctx.send("There is no game going on.")
      return
  athiap=str(inactivep.id)
  athap=str(activep.id)
  if athiap not in data['signedup']:
    await ctx.send("That person is not in game.")
    return
  if athap in data['players']:
    await ctx.send("That person is already in game.")
    return
  #
  await pkill(ctx,inactivep)
  data['players'][athap]={}
  data['players'][athap]['incc']=[]
  guildd=bot.get_guild(448888674944548874)
  role = discord.utils.get(guildd.roles, name="Players")
  await activep.add_roles(role)
  role = discord.utils.get(guildd.roles, name="Alive")
  await activep.add_roles(role)
  data['signedup'][athap] = 1
  data['signedup'].pop(athiap)
  data['money'][athap]=data['money'][athiap]
  data['players'][athap]['role']=data['players'][athiap]['role']
  data['players'][athap]['team']=data['players'][athiap]['team']
  data['players'][athap]['state']=1
  data['players'][athap]['msg']=0
  data['players'][athap]['inv']=[]
  for item in data['players'][athiap]['inv']:
      data['players'][athap]['inv'].append(item)
  #
  teamchat=discord.utils.get(guildd.channels,name=data['players'][athap]['team'])
  await teamchat.set_permissions(activep, read_messages=True,send_messages=True,add_reactions=True)
  data['players'][athap]['incc'].append(teamchat.id)
  
  #
  for channel in data['chnls']:
    if data['chnls'][channel]['owner']==int(athiap):
      data['chnls'][channel]['owner']=int(athap)
  for channel in data['players'][athiap]['incc']:
      data['players'][athap]['incc'].append(channel)
      chnl = discord.utils.get(guildd.channels,id=channel)
      await chnl.set_permissions(activep, read_messages=True,send_messages=True,add_reactions=True)
  #
  roleid= data['players'][athap]['role']
  rolename=data['rt'][roleid]['lirole']
  chnlname = str(data['players'][athap]['team']) + "_" + str(rolename)
  chnlname=chnlname.replace(' ','-')
  chnl = discord.utils.get(guildd.channels,name=chnlname)
  await chnl.set_permissions(activep, read_messages=True,send_messages=True,add_reactions=True)
  await chnl.set_permissions(inactivep, read_messages=True,send_messages=False,add_reactions=True)
  data['smarket']['inv'][athap]={}
  data['smarket']['inv'][athap]['sun']=data['smarket']['inv'][athiap]['sun']
  data['smarket']['inv'][athap]['smirk']=data['smarket']['inv'][athiap]['smirk']
  data['smarket']['inv'][athap]['smile']=data['smarket']['inv'][athiap]['smile']
  data['smarket']['inv'][athap]['joy']=data['smarket']['inv'][athiap]['joy']
  data['smarket']['inv'][athap]['pens']=data['smarket']['inv'][athiap]['pens']
  dump()
  await ctx.send("Done.")

@bot.command()
@commands.has_role("Informer")
async def evall(ctx,*,thing:str):
    '''Eval command <Informer>'''
    #ctx=ctx
    '''try:
      res = eval(thing)
      if inspect.isawaitable(res):
            await res
            await ctx.send("Command executed!")
      else:
            #await ctx.send("Command executed!!")
            await ctx.send(res)
    except Exception as e:
        try:
          #thing=f'async def func():\n{textwrap.indent(thing, "  ")}'
          exec(thing)
          await ctx.send("Command executed!")
        except:
          await ctx.send(f"Eval failed! Exception - {e}")'''
    #rdanny's
    env = {
            'bot': bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            #'_': self._last_result
        }

    env.update(globals())
    stdout = io.StringIO()
    if thing.startswith('```') and thing.endswith('```'):
            a = '\n'.join(thing.split('\n')[1:-1])
            thing = a.strip('` \n')
    #await ctx.send(thing)
    to_compile = f'async def func():\n{textwrap.indent(thing, "  ")}'
    try:
            exec(to_compile, env)
    except Exception as e:
            await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
    func = env['func']
    try:
            #with redirect_stdout(stdout):
        ret = await func()
    except Exception as e:
            value = stdout.getvalue()
            #await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
            await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
    else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                #self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')
    


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
  ath = str(ctx.author.id)
  rolz=[]
  role1 = discord.utils.get(guildd.roles, name="Alive")
  role2 = discord.utils.get(guildd.roles, name="Respawning")
  role3 = discord.utils.get(guildd.roles, name="Signed-Up!")
  rolz.append(role1)
  rolz.append(role2)
  rolz.append(role3)
  for role in rolz:
    if role in ctx.author.roles:
      await ctx.send("It seems you might be in a game. Please wait for the game to get over before you can promote.")
      return
  role = discord.utils.get(guildd.roles, name="Helpers")
  await ctx.author.add_roles(role)
  role = discord.utils.get(guildd.roles, name="Helper")
  await ctx.author.remove_roles(role)
  await ctx.send("You have been promoted , {}".format(ctx.author.mention))

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

#host




@bot.command()
@commands.has_any_role("Helpers","Host")
async def poll(ctx,*,message):
    '''Creates a poll with yes or no. <Helper>'''
    poll = discord.Embed(colour=random.randint(0, 0xffffff))
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
@commands.has_any_role("Helpers","Host")
async def advancedpoll(ctx,timee:int,*,message):
    '''Creates a poll with yes or no to close it in a certain amount of time (Note that the bot closing will stop this from working). <Helper>'''
    poll = discord.Embed(colour=random.randint(0, 0xffffff))
    poll.set_author(name="POLL")
    poll.add_field(name="Reg:- ",value=message,inline="false")
    reac="\U0001f44d"
    reac2="\U0001f44e"
    reac3="⛔"
    a=await ctx.send(embed=poll)
    await a.add_reaction(reac)
    await a.add_reaction(reac2)
    await a.add_reaction(reac3)
    await asyncio.sleep(timee)
    yesn=0
    yesp=""
    non=0
    nop=""
    mehn=0
    mehp=""
    other=0
    otherp=""
    channel=a.channel
    msgid = a.id
    a = await channel.fetch_message(msgid)
    for reaction in a.reactions:
      print(reaction)
      if str(reaction)==reac:
        users = await reaction.users().flatten()
        for user in users:
          if user.id==450320950026567692:
            continue
          yesp+=f"{user.mention}"
        yesn+=reaction.count-1
      elif str(reaction)==reac2:
        users = await reaction.users().flatten()
        for user in users:
          if user.id==450320950026567692:
            continue
          nop+=f"{user.mention}"
        non+=reaction.count-1
      elif str(reaction)==reac3:
        users = await reaction.users().flatten()
        for user in users:
          if user.id==450320950026567692:
            continue
          mehp+=f"{user.mention}"
        mehn+=reaction.count-1
      else:
        users = await reaction.users().flatten()
        for user in users:
          if user.id==450320950026567692:
            continue
          otherp+=f"{user.mention} "
        other+=reaction.count
    cont= a.content + f"{yesn} ({yesp}) voted yes, {non} ({nop}) voted no and {mehn} ({mehp}) voted neither."
    if other>0:
       cont+=f" {other} ({otherp}) voted something that wasn't even an option."
    await a.edit(content=cont)
    
@bot.command(aliases=["rc"])
@commands.has_any_role("Helpers","Host")
async def removecash(ctx,member:typing.Union[discord.Member,str],cash):
    '''Removes a certain amount of cash from a person. <Helper>'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    guildd=ctx.message.guild
    if member in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(member)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      member = discord.utils.get(guildd.members,id=int(idd))
    elif isinstance(member,discord.member.Member):
      pass
    else:
      await ctx.send("Invalid User")
      return

    data['money'][str(member.id)]-=int(cash)
    await ctx.send("{} has been reduced from {}'s account. Current balance is {} .".format(cash,member.mention,data['money'][str(member.id)]))
    
@bot.command(aliases=["ac"])
@commands.has_any_role("Helpers","Host")
async def addcash(ctx,member:typing.Union[discord.Member,str],cash):
    '''Adds a certain amount of cash to a person's balance. <Helper>'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    guildd=ctx.message.guild
    if member in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(member)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      member = discord.utils.get(guildd.members,id=int(idd))
    elif isinstance(member,discord.member.Member):
      pass
    else:
      await ctx.send("Invalid User")
      return
    data['money'][str(member.id)]+=int(cash)
    await ctx.send("{} has been added to {}'s account. Current balance is {} .".format(cash,member.mention,data['money'][str(member.id)]))
    
@bot.command(aliases=["gso"])
@commands.has_any_role("Helpers","Host")
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
@commands.has_any_role("Helpers","Host")
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
@commands.has_any_role("Helpers","Host")
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
    data['lottery']+=500
    await ctx.send("Game has started with code {} !".format(code))
    await bot.change_presence(activity=discord.Game(name="A game is going on. It's day 0 now.", type=1))
    data['players']={}
    data['teams']=[]
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
@commands.has_any_role("Helpers","Host")
async def assignroles(ctx,code):
    '''Assigns roles and makes all channels. <Helpers>'''
    global data
    if int(gamestate) != 3:
        await ctx.send("The game hasn't started")
        return
    listoplayers = []
    rolelist=[]
    data['code']['gamephase']=0
    #
    guildd=ctx.message.guild
    rolem1 = discord.utils.get(guildd.roles, name="Host")
    role0 = discord.utils.get(guildd.roles, name="Helpers") 
    role1 = discord.utils.get(guildd.roles, name="Alive")
    role2 = discord.utils.get(guildd.roles, name="Respawning")
    role3 = discord.utils.get(guildd.roles, name="Dead")
    role4 = discord.utils.get(guildd.roles, name="Spectator")
    storymark = {
    guildd.default_role: discord.PermissionOverwrite(read_messages=False),
    guildd.me: discord.PermissionOverwrite(read_messages=True),
    rolem1: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role0: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role1: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role2: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role3: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role4: discord.PermissionOverwrite(read_messages=True,send_messages=False)
                 }
    batle = {
    guildd.default_role: discord.PermissionOverwrite(read_messages=False),
    guildd.me: discord.PermissionOverwrite(read_messages=True),
    rolem1: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role0: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role1: discord.PermissionOverwrite(read_messages=True,send_messages=True,add_reactions=True),
    role2: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role3: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role4: discord.PermissionOverwrite(read_messages=True,send_messages=False)
                 }
    resp = {
    guildd.default_role: discord.PermissionOverwrite(read_messages=False),
    guildd.me: discord.PermissionOverwrite(read_messages=True),
    rolem1: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role0: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role1: discord.PermissionOverwrite(read_messages=False,send_messages=False,add_reactions=True),
    role2: discord.PermissionOverwrite(read_messages=True,send_messages=True,add_reactions=True),
    role3: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role4: discord.PermissionOverwrite(read_messages=True,send_messages=False)
                 }
    deads = {
    guildd.default_role: discord.PermissionOverwrite(read_messages=False),
    guildd.me: discord.PermissionOverwrite(read_messages=True),
    rolem1: discord.PermissionOverwrite(read_messages=True,send_messages=True),
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
    markc = await guildd.create_text_channel('auction_house',overwrites=storymark,category=cate)
    pollc = await guildd.create_text_channel('voting_booth',overwrites=storymark,category=cate)
    respc = await guildd.create_text_channel('respawning',overwrites=resp,category=cate)      
    deadsc = await guildd.create_text_channel('dead-spec',overwrites=deads,category=cate) 
    msg = await batlec.send("This is the battlefield! Where warriors fight to death! \nOr sometimes like to chill out and chat.")
    await msg.pin()
    msg = await respc.send("Use !fghs to send messages in the battlefield for free.\nUse !ghs if you want to send clear messages in battlefield (This costs 25c)\nUse !tghs to send clear messages to your team.(This costs 100c)")
    await msg.pin()
    #
    rolem1 = discord.utils.get(guildd.roles, name="Host")
    role0 = discord.utils.get(guildd.roles, name="Helpers")
    role3 = discord.utils.get(guildd.roles, name="Dead")
    role4 = discord.utils.get(guildd.roles, name="Spectator")
    overwrites = {
    guildd.default_role: discord.PermissionOverwrite(read_messages=False),
    guildd.me: discord.PermissionOverwrite(read_messages=True),
    rolem1: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role0: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role3: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role4: discord.PermissionOverwrite(read_messages=True,send_messages=False)
                 }
    namee = str(data['code']['gamecode'])+' factions'
    await guildd.create_category(namee)
    cate = discord.utils.get(ctx.message.guild.categories, name=namee)
    for role in data['rt']:
      if data['rt'][role]['team'] not in data['teams']:
        data['teams'].append(data['rt'][role]['team'])

    for team in data['teams']:
      for role in data['rt']:
        if data['rt'][role]['team'] ==team:
          soloq=data['rt'][role]['soloq']


      teamchat=await guildd.create_text_channel(team,overwrites=overwrites,category=cate)
      
      data['building'][team]={}
      data['building'][team]['vault']=0
      data['building'][team]['trihouse']={}
      data['building'][team]['trihouse']['who']=""
      data['building'][team]['trihouse']['cash']=0
      if soloq==1:
        data['building'][team]['forge']=7
        data['building'][team]['market']=4
        data['building'][team]['trihouse']['eligible']=0
      else:
        data['building'][team]['forge']=1
        data['building'][team]['market']=1
        data['building'][team]['trihouse']['eligible']=1
      data['building'][team]['stash']={}
      data['building'][team]['stash']['items']=[]
      data['building'][team]['stash']['smoney']=0
      data['building'][team]['marketprices']=[]
      data['building'][team]['marketprices'].append("Placeholder")
      data['building'][team]['marketprices'].append(1000)
      data['building'][team]['marketprices'].append(1000)
      data['building'][team]['marketprices'].append(1000)
      data['building'][team]['marketprices'].append(2000)
      data['building'][team]['marketprices'].append(2000)
      data['building'][team]['marketprices'].append(2000)
      data['building'][team]['marketprices'].append(3000)
      data['building'][team]['marketprices'].append(3000)
      data['building'][team]['marketprices'].append(3000)
      data['building'][team]['marketprices'].append(4000)

      teammsg=discord.Embed(colour=random.randint(0, 0xffffff))
      teammsg.set_author(name="Team info!")
      teammsg.add_field(name="Welcome!",value=f"You are all members of the {team} team! \n Work together and win this game!")
      msg= await teamchat.send(embed=teammsg)
      await msg.pin()

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
        data['players'][user]['msg']=0
        data['players'][user]['inv']=[]
        data['players'][user]['emoji']=data['signedup'][user]['emoji']
        #print(data)
        num+=1
    #print(data)
    #
    for user in data['players']:
        guildd=bot.get_guild(448888674944548874)
        userr=discord.utils.get(guildd.members,id=int(user))
        roleinfo=discord.Embed(colour=random.randint(0, 0xffffff))
        roleinfo.set_author(name="Role info!")
        roleinfo.add_field(name="This message has been sent to you to inform you of the role you have in the next up coming game in the Colour Battles server!",value="**Your role for this game is `{}` and you are in the team `{}`!** \n You are **__not__** allowed to share this message! \n You are **__not__** allowed to share the screenshot of this message! \n Breaking any of these rules can result in you being banned from the server.".format(data['players'][user]['role'],data['players'][user]['team']),inline="false")
        roleinfo.add_field(name="If you need help reagrding this role or this game , please make sure to contact the Informers or the Helpers or read the role info from from the #role_info channel.",value="Have a good game!\n *I am a bot and this action has been done automatically. Please contact the informer if anything is unclear.* ",inline="false")
        data['money'][user]=0
        try:
          await userr.send(embed=roleinfo)
        except:
          print("Dm denied")
        #getchatandsetperm

        teamchat=discord.utils.get(guildd.channels,name=data['players'][user]['team'])
        await teamchat.set_permissions(userr, read_messages=True,send_messages=True,add_reactions=True)
        #this stops them from tam chat talking
        #data['players'][str(user)]['incc'].append(teamchat.id)
        
        roleid= data['players'][user]['role']
        rolename=data['rt'][roleid]['lirole']
        chnlname = str(data['players'][user]['team']) + "_" + str(rolename)
        chnl = await guildd.create_text_channel(chnlname,overwrites=overwrites,category=cate)
        await chnl.set_permissions(userr, read_messages=True,send_messages=True,add_reactions=True)
        role = data['players'][user]['role']
        rolet=data['rt'][str(role)]['lirole']
        msg=  await rolehelp(rolet,chnl)
        await msg.pin()
        #data['players'][str(user)]['incc'].append(chnl.id) THIS DISABLES PEOPLE FROM TALKING IN CHAT WHEN DEAD
    await listallr(ctx)
    dump()    
    
@bot.command(aliases=["a"])
@commands.has_any_role("Helpers","Host")
async def listallr(ctx):
    '''Lists everyone's roles. <Helpers>'''
    temp = ""
    for user in data['players']:
        guildd=bot.get_guild(448888674944548874)
        userr=discord.utils.get(guildd.members,id=int(user))
        temp +="{} has the role `{}` \n".format(userr.mention,data['players'][user]['role'])
    msg = await ctx.send("​")
    await msg.edit(content=temp)


@bot.command(aliases=["ar"])
@commands.has_any_role("Helpers","Host")
async def addrole(ctx,role,team,soloq=0,*,litrole):
    '''Adds roles to the role list.(Similar roles must be entered with a number after them , teams can anything, but repeat teams will make them have the same teams. Solos need to have a different team. <Helpers>'''
    if (int(gamestate) >= 3):
        await ctx.send("A game is already going on.")
        return
    if role in data['roles']:
      await ctx.send(f"`{role}` already exists. Please use another name.")
      return
    data['roles'].append(role)
    data['rt'][role]={}
    data['rt'][role]['team']=team.lower()
    data['rt'][role]['lirole'] = litrole
    # 0 or not solo, 1 for solo
    data['rt'][role]['soloq'] = soloq
    await ctx.send("{} added for the team {}.".format(role,team))
    dump()
    
@bot.command(aliases=["rr"])
@commands.has_any_role("Helpers","Host")
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
@commands.has_any_role("Helpers","Host")
async def listroles(ctx):
    '''Prints the entire role list. <Helpers>'''
    temp="The rolelist is - \n"
    num=0
    for role in data['roles']:
        num+=1
        temp +="{} of {}\n".format(role,data['rt'][role])
    temp+="The number of roles is "+str(num)
    if len(temp)>2000:
      a=temp[:2000]
      b=temp[2000:]
      am=await ctx.send("​")
      await am.edit(content=a)
      bm=await ctx.send("​")
      await bm.edit(content=b)
    else:
      msg = await ctx.send("​")
      await msg.edit(content=temp)
    
@bot.command(aliases=["cr"])
@commands.has_any_role("Helpers","Host")
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
@commands.has_any_role("Helpers","Host")
async def endgame(ctx):
    '''Ends the game. <Helpers>'''
    global gamestate
    global data
    if int(gamestate)!=3:
        await ctx.send("A game isn't even going on.")
        return
    gamestate=4
    data['gamestate']=4
    await bot.change_presence(activity=discord.Game(name="Game concluded!", type=1))
    for user in data['players']:
        guildd=bot.get_guild(448888674944548874)
        userr=discord.utils.get(guildd.members,id=int(user))
        role = discord.utils.get(guildd.roles, name="Spectator")
        await userr.add_roles(role)
    await ctx.send("The game has ended!")
    dump()
    
@bot.command(aliases=["k"])
@commands.has_any_role("Helpers","Host")
async def kill(ctx,user:typing.Union[discord.Member,str]):
    '''Sets a person's status as respawning in game. <Helpers>'''
    if int(gamestate)!=3:
        await ctx.send("There isn't a game going on.")
        return
    guildd=bot.get_guild(448888674944548874)
    if user in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(user)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      user = discord.utils.get(guildd.members,id=int(idd))
    elif isinstance(user,discord.member.Member):
      pass
    else:
      await ctx.send("Invalid User")
      return
    data['players'][str(user.id)]['state']=0
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
@commands.has_any_role("Helpers","Host")
async def respawn(ctx,user:typing.Union[discord.Member,str]):
    '''Respawns a person in game <Helpers>'''
    if int(gamestate)!=3:
        await ctx.send("There isn't a game going on.")
        return
    guildd=ctx.message.guild
    if user in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(user)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      user = discord.utils.get(guildd.members,id=int(idd))
    elif isinstance(user,discord.member.Member):
      pass
    else:
      await ctx.send("Invalid User")
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
@commands.has_any_role("Helpers","Host")
async def pkill(ctx,user:typing.Union[discord.Member,str]):
    '''Kills a person permanently in game. <Helpers>'''
    if int(gamestate)!=3:
        await ctx.send("There isn't a game going on.")
        return
    guildd=bot.get_guild(448888674944548874)
    if user in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(user)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      user = discord.utils.get(guildd.members,id=int(idd))
    elif isinstance(user,discord.member.Member):
      pass
    else:
      await ctx.send("Invalid User")
      return
    data['players'][str(user.id)]['state']=0
    role = discord.utils.get(guildd.roles, name="Respawning")
    await user.remove_roles(role)
    role = discord.utils.get(guildd.roles, name="Alive")
    await user.remove_roles(role)
    role = discord.utils.get(guildd.roles, name="Dead")
    await user.add_roles(role)
    for cc in data['players'][str(user.id)]['incc']:
        chnl = bot.get_channel(int(cc))
        await chnl.set_permissions(user, read_messages=True,send_messages=False,add_reactions=False)
    ath = str(user.id)
    if ath in data['marketalert']:
      data['marketalert'].remove(ath)
    await ctx.send("Permanently killed {}.".format(user.mention))
    dump()


@bot.command(aliases=["mg"])
@commands.has_any_role("Helpers","Host")
async def massgive(ctx,cash=100):
  '''Gives a certain amount of cash to everyone who has an account. <Helpers>'''
  global data
  if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  for  ath in data['money']:
    team=str(data['players'][ath]['team'])
    add=cash*data['building'][team]['forge']
    try:
      if ath not in data['smarket']['inv']:
        data['smarket']['inv'][ath]={}
        data['smarket']['inv'][ath]['sun']=0
        data['smarket']['inv'][ath]['smirk']=0
        data['smarket']['inv'][ath]['smile']=0
        data['smarket']['inv'][ath]['joy']=0
        data['smarket']['inv'][ath]['pens']=0
      add+=int(data['smarket']['inv'][ath]['sun']*data['smarket']['stocks']['sun']*0.03)
      add+=int(data['smarket']['inv'][ath]['smirk']*data['smarket']['stocks']['smirk']*0.03)
      add+=int(data['smarket']['inv'][ath]['smile']*data['smarket']['stocks']['smile']*0.03)
      add+=int(data['smarket']['inv'][ath]['joy']*data['smarket']['stocks']['joy']*0.03)
      add+=int(data['smarket']['inv'][ath]['pens']*data['smarket']['stocks']['pens']*0.03)
      data['money'][ath]+=int(add)
    except:
      print("The stock market hasn't been created , that part was skipped.")
      data['money'][ath]+=int(add)
  await ctx.send("Added the cash to everyone who had an account.")
  dump()

@bot.command(aliases=["mbal"])
@commands.has_any_role("Helpers","Host")
async def masterbalance(ctx,member:typing.Union[discord.Member,str]):
  '''Allows to see the balance of another player <Helpers>'''
  if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  guildd=ctx.message.guild
  if member in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(member)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      member = discord.utils.get(guildd.members,id=int(idd))
  elif isinstance(member,discord.member.Member):
      pass
  else:
      await ctx.send("Invalid User")
      return
  id=str(member.id)
  await ctx.send("{}'s balance is {}.".format(member.mention,data['money'][id]))

@bot.command(aliases=["minv"])
@commands.has_any_role("Helpers","Host")
async def masterinventory(ctx,member:typing.Union[discord.Member,str]):
  '''Allows to see the inventory of another player <Helpers>'''
  if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  guildd=ctx.message.guild
  if member in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(member)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      member = discord.utils.get(guildd.members,id=int(idd))
  elif isinstance(member,discord.member.Member):
      pass
  else:
      await ctx.send("Invalid User")
      return
  ath=str(member.id)
  msg="That inventory contains-\n"
  for item in data['players'][ath]['inv']:
    msg+=f"{item}\n"
  await ctx.send(msg)

@bot.command(aliases=["ca"])
@commands.has_any_role("Helpers","Host")
async def createauction(ctx,name,strtbid,*,text):
    '''Allows the user to create a auction <Helpers>'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    global data
    guildd=bot.get_guild(448888674944548874)
    mark=discord.utils.get(guildd.channels,name="auction_house")
    data['auction']['state']=1
    await mark.send("__**ITEM - {}**__".format(name))
    await mark.send("Perks - {}".format(text))
    aucmsg = await mark.send(f"Current bid - {strtbid} - Starting Value")
    data['auction']['msg']=str(aucmsg.id)
    data['auction']['chn']=str(aucmsg.channel.id)
    data['auction']['bid']=int(strtbid)
    data['auction']['bider']=""
    data['auction']['bidern']=""
    data['auction']['item']=name
    data['auction']['perks']=text
    dump()

@bot.command(aliases=["cla"])
@commands.has_any_role("Helpers","Host")
async def closeauction(ctx):
  '''Allows the user to close a auction <Helpers>'''
  if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  global data
  if data['auction']['state']==0:
    await ctx.send("There is no auction going on right now.")
    return
  await ctx.send("The market is closing!")
  while True:
    a=data['auction']['bid']
    await asyncio.sleep(30)
    if a==data['auction']['bid']:
      break
  guildd=bot.get_guild(448888674944548874)
  mark=discord.utils.get(guildd.channels,name="auction_house")
  if data['auction']['bider'] == "":
    await mark.send("There were no bids, as such this item has been sold to no one.")
  else:
    who=data['auction']['bidern']
    cost=data['auction']['bid']
    await mark.send("Congrats! {} has won the item auctioned for {} ! ".format(who,cost))
    whop=data['auction']['bider']
    #stuff
    team=data['players'][whop]['team']
    data['building'][team]['vault']-=cost
    data['building'][team]['stash']['smoney']-=cost
    data['building'][team]['stash']['items'].append(data['auction']['item'])
  data['auction']['state']=0
  data['auction']['msg']=""
  data['auction']['chn']=""
  data['auction']['bid']=0
  data['auction']['bider']=""
  data['auction']['bidern']=""
  data['auction']['item']=""
  data['auction']['perks']=""
  dump()

@bot.command(aliases=["cba"])
@commands.has_any_role("Helpers","Host")
async def createblindauction(ctx,name,strtbid,*,text):
    '''Allows the user to create a blind auction <Helpers>'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    global data
    guildd=bot.get_guild(448888674944548874)
    mark=discord.utils.get(guildd.channels,name="auction_house")
    code=chr(random.randint(97, 122))+chr(random.randint(97, 122))+chr(random.randint(97, 122))
    if code not in data['bauction']:
      data['bauction'][code]={}
      data['bauction'][code]['biders']={}
      data['bauction'][code]['item']=name
      data['bauction'][code]['perks']=text
      data['bauction'][code]['minvalue']=int(strtbid)
    auction = discord.Embed(colour=random.randint(0, 0xffffff))
    auction.set_author(name="BLIND AUCTION")
    auction.add_field(name=f"__**ITEM - {name}**__",value=f"**Code- {code}**\nPerks - {text}\nMin value - {strtbid}",inline="false")
    await mark.send(embed=auction)
    dump()
    

@bot.command(aliases=["clba"])
@commands.has_any_role("Helpers","Host")
async def closeblindauction(ctx,code):
  '''Allows the user to close a auction <Helpers>'''
  if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  global data
  if code not in data['bauction']:
    await ctx.send("Invalid Code.")
    return
  cost=0
  whop=""
  for person in data['bauction'][code]['biders']:
    data['building'][str(person)]['stash']['smoney']-=data['bauction'][code]['biders'][person]
    if data['bauction'][code]['biders'][person]>cost:
      cost=data['bauction'][code]['biders'][person]
      whop=person
  
  guildd=bot.get_guild(448888674944548874)
  mark=discord.utils.get(guildd.channels,name="auction_house")
  if whop=="" and cost==0:
    await mark.send(f"There were no bids on the item with code {code}, as such this item has been sold to no one.")
  else:
    await mark.send(f"Congrats! The item auctioned for {cost} ! (Code was {code})")
    team=str(whop)
    data['building'][team]['vault']-=cost
    
    data['building'][team]['stash']['items'].append(data['bauction'][code]['item'])
  data['bauction'].pop(code)
  dump()


@bot.command(aliases=["rmm"])
@commands.has_any_role("Helpers","Host")
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
@commands.has_any_role("Helpers","Host")
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
@commands.has_any_role("Helpers","Host")
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
  data['smarket']['stocks']['smile']=250
  data['smarket']['stocks']['joy']=100
  data['smarket']['stocks']['pens']=50
  data['smarket']['trades']={}
  data['smarket']['trades']['sun']=0
  data['smarket']['trades']['smirk']=0
  data['smarket']['trades']['smile']=0
  data['smarket']['trades']['joy']=0
  data['smarket']['trades']['pens']=0
  guildd=bot.get_guild(448888674944548874)
  mark=discord.utils.get(guildd.channels,name="auction_house")
  smarket = await mark.send("Cost of :sunglasses: is 1000 \nCost of :smirk: is 500 \nCost of :smiley: is 250 \nCost of :joy: is 100 \nCost of :pensive: is 50 \n")
  await smarket.pin()
  data['smarket']['msg']=str(smarket.id)
  data['smarket']['chn']=str(smarket.channel.id)
  dump()

@bot.command(aliases=["chngmm"])
@commands.has_any_role("Helpers","Host")
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

@bot.command()
@commands.has_any_role("Helpers","Host")
async def msgcount(ctx):
  '''Used to check how many messages were sent by who during the duration of the game.'''
  msg = await ctx.send("Loading.")
  count="The message count is - \n"
  for ath in data['players']:
    count+="<@{}> has sent {}.\n".format(ath,data['players'][ath]['msg'])
  await msg.edit(content=count)

@bot.command(aliases=["addinv"])
@commands.has_any_role("Helpers","Host")
async def addtoinv(ctx,user:typing.Union[discord.Member,str],*,item):
  '''Use this to add something to a person's inventory <Helpers>'''
  if int(gamestate)!=3:
      await ctx.send("There is no game going on right now.")
      return
  guildd=ctx.message.guild
  if user in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(user)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      user = discord.utils.get(guildd.members,id=int(idd))
  elif isinstance(user,discord.member.Member):
      pass
  else:
      await ctx.send("Invalid User")
      return
  ath=str(user.id)
  data['players'][ath]['inv'].append(item)
  await ctx.send("Done.")

@bot.command(aliases=["reminv"])
@commands.has_any_role("Helpers","Host")
async def removefrominv(ctx,user:typing.Union[discord.Member,str],*,item):
  '''Use this to remove something from someone's inventory. <Helpers>'''
  if int(gamestate)!=3:
      await ctx.send("There is no game going on right now.")
      return
  guildd=ctx.message.guild
  if user in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(user)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      user = discord.utils.get(guildd.members,id=int(idd))
  elif isinstance(user,discord.member.Member):
      pass
  else:
      await ctx.send("Invalid User")
      return
  ath=str(user.id)
  try:
    data['players'][ath]['inv'].remove(item)
  except ValueError:
    await ctx.send("That item was not found in their inventory.")
    return
  await ctx.send("Done.")

@bot.command(aliases=["endt"])
@commands.has_any_role("Helpers","Host")
async def endtribute(ctx):
  '''Use this to commence the tributing. <Helper>'''
  if int(gamestate)!=3:
      await ctx.send("There is no game going on right now.")
      return

  info={}
  lowest=99999
  lowestteam=""
  for team in data['teams']:
    if data['building'][team]['trihouse']['eligible']==0: 
      pass
    else:
      info[team]=data['building'][team]['trihouse']['cash']
      data['building'][team]['vault']-=data['building'][team]['trihouse']['cash']
      if data['building'][team]['trihouse']['cash'] <=lowest:
        lowestteam=team
        lowest=data['building'][team]['trihouse']['cash']
  sort = sorted(info.items(),key = lambda x:x[1],reverse=True)
  print(sort)
  text=""
  for entry in sort:
	  text+=f"{entry[0]} paid {entry[1]} \n"
  
  try:
    who=str(data['building'][lowestteam]['trihouse']['who'])
    guildd=bot.get_guild(448888674944548874)
    user=discord.utils.get(guildd.members,id=int(who))
    await kill(ctx,user)
    who=user.mention
  except:
    who="Someone Random"
    await ctx.send("The lowest team has not set a tribute, got None as a person. Please procede to kill someone random.")

  triinfo = discord.Embed(colour=discord.Colour.red())
  triinfo.set_author(name="Tribute Info-")
  triinfo.add_field(name="Who is dying?-",value=f"**{who} was killed.**",inline="false")
  triinfo.add_field(name="Who paid the most and the least?",value=text,inline="false")
  for team in data['teams']:
    data['building'][team]['trihouse']['who']=""
    data['building'][team]['stash']['smoney']-=data['building'][team]['trihouse']['cash']
    data['building'][team]['trihouse']['cash']=0
  await ctx.send(embed=triinfo)
  dump()

@bot.command(aliases=["ap"])
@commands.has_any_role("Helpers","Host")
async def advancephase(ctx,cost=100):
  """ Use this command to advance the game phase.

  Use this by typing !advancephase
  
  """
  global data
  guildd=bot.get_guild(448888674944548874)
  if int(gamestate)!=3:
        await ctx.send("There isn't a game going on.")
        return
  data['code']['gamephase']+=1
  num = data['code']['gamephase']
  if num %2==0:
    text = f"Day {int(num/2)}"
  else:
    text = f"Night {int((num+1)/2)}"
  namee= str(data['code']['gamecode']) + ' factions'
  cate = discord.utils.get(ctx.message.guild.categories, name=namee)
  for channel in cate.channels:
      msg = await channel.send(f"**__          {text}          __**")
      await msg.pin()
  townc=discord.utils.get(guildd.channels,name="battlefield")
  msg = await townc.send(f"**__          {text}          __**\n<@&748375810498625597>")
  await msg.pin()
  await bot.change_presence(activity=discord.Game(name=f"A game. It's {text} now.", type=1))
  await massgive(ctx,cash=cost)
  data['lottery']+=500
  dump()

@bot.command(aliases=["cp"])
@commands.has_any_role("Helpers","Host")
async def createpoll(ctx):
  '''Allows the host to create a poll. <Helper>'''
  global data
  if int(gamestate) != 3:
    await ctx.send("There is no game going on right now.")
    return
  guildd=bot.get_guild(448888674944548874)
  code=chr(random.randint(97, 122))+chr(random.randint(97, 122))+chr(random.randint(97, 122))
  temp = ""
  temp+=f"Poll `{code}`- \n"
  emjlist=[]
  an=0
  for member in data['players']:
      if data['players'][member]['state']==1:
        an+=1
  pages=math.ceil(an/15)
  if pages==1:
    for member in data['players']:
      if data['players'][member]['state']==1:
        person = discord.utils.get(guildd.members,id=int(member))
        temp +=f"{data['signedup'][member]['emoji']} - <@{member}> ({person.name}) \n"
        emjlist.append(data['signedup'][member]['emoji'])
    msg = await ctx.send(temp)
    for emoji in emjlist:
      await msg.add_reaction(emoji)
    data['poll'][code]={}
    data['poll'][code]['pages']=1
    data['poll'][code]['msgid']=[]
    data['poll'][code]['msgid'].append(str(msg.id))
    data['poll'][code]['chnlid']=str(msg.channel.id)
  else:
    for member in data['players']:
      if data['players'][member]['state']==1:
        person = discord.utils.get(guildd.members,id=int(member))
        temp +=f"{data['signedup'][member]['emoji']} - <@{member}> ({person.name}) \n"
        emjlist.append(data['signedup'][member]['emoji'])
    data['poll'][code]={}
    data['poll'][code]['pages']=pages
    data['poll'][code]['msgid']=[]
    data['poll'][code]['chnlid']=str(ctx.message.channel.id)
    lineslist = temp.splitlines(True)
    await ctx.send(lineslist[0])
    for i in range(1,an+1,15): 
      msg=""
      for j in range(i,i+15): 
        if j>an:
          break
        msg+=lineslist[j]

      msgg = await ctx.send(msg)
      for j in range(i,i+15):
        if j>an:
          break
        await msgg.add_reaction(emjlist[j-1])
      data['poll'][code]['msgid'].append(str(msgg.id))
  dump()

@bot.command(aliases=["clp"])
@commands.has_any_role("Helpers","Host")
async def closepoll(ctx,code):
    '''Command that allows you to close polls. <Helper>'''
    global data
    number=0
    text=""
    tempmsg=f"Results for {code}-\n\n"
    guildd=bot.get_guild(448888674944548874)
    channel=discord.utils.get(guildd.channels,id=int(data['poll'][code]['chnlid']))

    reacted={}
    for msgid in data['poll'][code]['msgid']:
    #doublercheck
      a = await channel.fetch_message(msgid)
      for reaction in a.reactions:
          users = await reaction.users().flatten()
          for user in users:
                if user.id==450320950026567692:
                  continue
                if user.id in reacted:
                  reacted[user.id].append(reaction)
                else:
                  reacted[user.id]=[]
                  reacted[user.id].append(reaction)

    
    for people in reacted:
        who=discord.utils.get(guildd.members,id=int(people))
        if len(reacted[people])>1:
          for msgid in data['poll'][code]['msgid']:
            try:
              a = await channel.fetch_message(msgid)
              for emoji in reacted[people]:
                await a.remove_reaction(emoji, who)
            except:
              pass




    for msgid in data['poll'][code]['msgid']:
      emjlist=[]

      for member in data['players']:
        if data['players'][member]['state']==1:
          emjlist.append(data['signedup'][member]['emoji'])

      a = await channel.fetch_message(msgid)
      for emoji in emjlist:
        for reaction in a.reactions:
          if str(reaction)==emoji:
            for member in data['players']:
              if emoji==data['players'][member]['emoji']:
                who=discord.utils.get(guildd.members,id=int(member))
            users = await reaction.users().flatten()
            for user in users:
              if user.id==450320950026567692:
                continue
              text+=f"{user.mention} "
            number+=reaction.count-1
            if number==0:
              continue
            tempmsg+= f"For {who.mention} ({emoji}) - \n {number} - {text} \n\n"
            number=0
            text=""
      await a.clear_reactions()
    data['poll'].pop(code)
    await ctx.send(tempmsg)
    dump()

@bot.command(aliases=["lc","closechat","archivechat","archat"])
@commands.has_any_role("Helpers","Host")
async def lockchat(ctx):
    '''Use this to lock the chat, to move it into a separate category <Helper>'''
    global data
    if int(gamestate) != 3:
      await ctx.send("There is no game going on right now.")
      return
    guildd=ctx.message.guild
    name=data['code']['gamecode'] +' archive'
    category=discord.utils.get(guildd.categories, name=name)

    rolem1 = discord.utils.get(guildd.roles, name="Host")
    role0 = discord.utils.get(guildd.roles, name="Helpers") 
    role1 = discord.utils.get(guildd.roles, name="Alive")
    role2 = discord.utils.get(guildd.roles, name="Respawning")
    role3 = discord.utils.get(guildd.roles, name="Dead")
    role4 = discord.utils.get(guildd.roles, name="Spectator")
    archive = {
    guildd.default_role: discord.PermissionOverwrite(read_messages=False),
    guildd.me: discord.PermissionOverwrite(read_messages=True),
    rolem1: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role0: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role1: discord.PermissionOverwrite(read_messages=False),
    role2: discord.PermissionOverwrite(read_messages=False),
    role3: discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role4: discord.PermissionOverwrite(read_messages=True,send_messages=False)
                 }
    
    if category==None:
      category=await guildd.create_category(name)
    chnl=ctx.message.channel
    await chnl.edit(category=category,overwrites=archive)
    pins=[]
    async for message in chnl.history(limit=10000):
        if message.pinned:
          pins.append(message.content)
    msg=""
    for thing in pins[::-1]:
      msg+="\n- "+thing
    await ctx.send(f"Done, Pins are- `{msg}`")
    dump()
    
@bot.command(aliases=["toggletri","ttri"])
@commands.has_any_role("Helpers","Host")
async def toggletribute(ctx,team):
    global data
    if int(gamestate) != 3:
      await ctx.send("There is no game going on right now.")
      return
    if team not in data['building']:
      await ctx.send("That is not a valid team.")
      return
    if data['building'][team]['trihouse']['eligible']==1:
      data['building'][team]['trihouse']['eligible']=0
      await ctx.send(f"{team}'s tribute eligibility has been set to False. They will no longer be accounted for.")
    else:
      data['building'][team]['trihouse']['eligible']=1
      await ctx.send(f"{team}'s tribute eligibility has been set to True. They will be accounted for in tribute.")
    dump()

#\:sunglasses:\:smirk:\:smiley:\:joy:\:pensive:
#all
@bot.command()
async def ping(ctx):
    '''Returns Pong.'''
    print("Pong!")
    await ctx.send("Pong!")
    dump()
    
@bot.command()
async def timer(ctx,timee:int):
  '''Allows you to set an alarm. (WARNING - Existing timers will be erased if the bot resets. Use with caution)'''
  if timee > 36000:
    await ctx.send("You cannot set reminders greater than 10 hours.")
    return
  if timee<=0:
    await ctx.send("I cannot travel back in time.")
    return
  await ctx.send("I'll ping you in {} seconds.".format(timee))
  await asyncio.sleep(timee)
  await ctx.send("{}, here is your reminder of {} seconds.".format(ctx.author.mention,timee))


@bot.command(aliases=["j","join"])
async def signup(ctx,emoji="Emoji"):
    '''Allows you to signup for a game.Sign out by typing the command again.'''
    global data
    if (int(gamestate) != 1):
        await ctx.send("Sign ups are closed right now. Try joining when they are open , or after the game has concluded. Contact a Informer or a helper if you need help.")
        return
    ath=str(ctx.author.id) 
    if not ath in data['signedup']:
      if not ath in data['specters']:
        #check if host
        guildd=ctx.message.guild
        rolz=[]
        role1 = discord.utils.get(guildd.roles, name="Host")
        role2 = discord.utils.get(guildd.roles, name="Helpers")
        role3 = discord.utils.get(guildd.roles, name="Signed-Up!")
        rolz.append(role1)
        rolz.append(role2)
        rolz.append(role3)
        for role in rolz:
          if role in ctx.author.roles:
            await ctx.send("It seems you might have roles that are meant to run the game. Please demote before you can play.")
            return
        #check emoji
        if emoji not in emj.UNICODE_EMOJI["en"]:
          await ctx.send("That is not a valid emoji.")
          return
        for people in data['signedup']:
          if emoji == data['signedup'][people]['emoji']:
            await ctx.send("That emoji has already been used. Please pick another one.")
            return
        data['signedup'][ath] = {}
        data['signedup'][ath]['emoji'] = emoji
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
    guildd=bot.get_guild(448888674944548874)
    temp = ""
    tempno=0
    temp+="The list of people signed-up is - \n"
    for member in data['signedup']:
        tempno+=1
        person = discord.utils.get(guildd.members,id=int(member))
        temp +=f"{data['signedup'][member]['emoji']} - <@{member}> ({person.name}) \n"
    temp += "The number of people signed up is {} \n".format(tempno)
    msg = await ctx.send("​")
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
async def freeghostsay(ctx,*,fmsg):
    '''Use to send messages into town hall as a ghost for free!! <Respawning>'''
    guildd=bot.get_guild(448888674944548874)
    townc=discord.utils.get(guildd.channels,name="battlefield")
    taboo = "@everyone"
    taboo2="<@&722504160691355679>"
    taboo3="<@&748375810498625597>"
    taboo4="@here"
    if taboo in str(fmsg) or taboo2 in str(fmsg) or taboo3 in str(fmsg) or taboo4 in str(fmsg):
      await ctx.send("Please don't ping @ everyone.")
    else:
      alpha=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','1','2','3','4','5','6','7','8','9','0']
      num=random.randint(0, 10)
      for a in range(num):
        fmsg=fmsg.replace(random.choice(alpha),'o')
      for a in range(num):
        fmsg=fmsg.replace(random.choice(alpha),'p')
      for a in range(num):
        fmsg=fmsg.replace(random.choice(alpha),'.')
      for a in range(num):
        fmsg=fmsg.replace(random.choice(alpha),'OOOO')
      await townc.send("<Ghost> {}".format(fmsg))
    '''ghosthook = Webhook('https://discordapp.com/api/webhooks/723763897764675616/9c5GmG9WKemUjWv4cEMGVfHrjjmExGvV36JmS38Hep5KqK4nOKYfayzr6OTIQa2rgZ_O')
    ghosthook.send(msg)'''
   
@bot.command(aliases=["ghs"])
@commands.has_role("Respawning")
async def ghostsay(ctx,*,msg):
    '''Use this to send messages into town hall as a ghost for a price of 25c <Respawning>'''
    global data
    guildd=bot.get_guild(448888674944548874)
    townc=discord.utils.get(guildd.channels,name="battlefield")
    taboo = "@everyone"
    taboo2="<@&722504160691355679>"
    taboo3="<@&748375810498625597>"
    taboo4="@here"
    if taboo in str(msg) or taboo2 in str(msg) or taboo3 in str(msg) or taboo4 in str(msg):
      await ctx.send("Please don't ping @ everyone.")
    else:
      if data['money'][str(ctx.author.id)] <25:
        await ctx.send("You cannot afford to send this message.")
        return
      ath=str(ctx.author.id)
      data['money'][ath]-=25
      await townc.send("<Ghost> {}".format(msg))
    dump()

@bot.command(aliases=["tghs"])
@commands.has_role("Respawning")
async def teamsay(ctx,*,msg):
    '''Use this to send messages to your team as a ghost for 100c.<Respawning>'''
    global data
    guildd=bot.get_guild(448888674944548874)
    #townc=discord.utils.get(guildd.channels,name="battlefield")
    taboo = "@everyone"
    if taboo in str(msg):
      await ctx.send("Please don't ping @ everyone.")
    else:
      if data['money'][str(ctx.author.id)] <100:
        await ctx.send("You cannot afford to send this message.")
        return
      ath=str(ctx.author.id)
      data['money'][ath]-=100
      try:
        team=data['players'][str(ctx.author.id)]['team'] 
        teamc=discord.utils.get(guildd.channels,name=team)
        await teamc.send("<Ghost> {}".format(msg))
      except:
        print("There was some error.")
    dump()

@bot.command(aliases=["cc"])
@commands.has_role("Alive")
async def createchannel(ctx,ccname,*member:typing.Union[discord.Member,str]):
    '''Used to create a communication channel. Costs 50c.'''
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
      if people in emj.UNICODE_EMOJI["en"]:
        idd=emjtop(people)
        if idd== None:
          await ctx.send(f"Invalid Emoji {people}.")
          return
        people = discord.utils.get(guildd.members,id=int(idd))
      elif isinstance(people,discord.member.Member):
        pass
      else:
        await ctx.send(f"Invalid Input {people}.")
        return
      if data['players'][str(people.id)]['state']==0:
        await ctx.send("You cannot make ccs with the dead.")
        return
      if people==ctx.author:
        await ctx.send("You cannot make a cc with you as a member. You are included by deafult.")
        return
      if str(people.id) not in data['signedup']:
        await ctx.send("That person is not in this game.")
        return
    if ccname=="battlefield" or ccname=="respawning" or ccname=="auction_house":
      await ctx.send("You cannot name a cc that.")
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
    rolem1 = discord.utils.get(guildd.roles, name="Host")
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
    rolem1: discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role0:discord.PermissionOverwrite(read_messages=True,send_messages=True),
    role3:discord.PermissionOverwrite(read_messages=True,send_messages=False),
    role4:discord.PermissionOverwrite(read_messages=True,send_messages=False)
                 }
    a = await guildd.create_text_channel(str(ccname),overwrites=overwrites,category=cate)
    plist=""
    plist+="<@{}> \n".format(author.id)
    for people in member:
      if people in emj.UNICODE_EMOJI["en"]:
        idd=emjtop(people)
        if idd== None:
          await ctx.send(f"Invalid Emoji {people}.")
          return
        people = discord.utils.get(guildd.members,id=int(idd))
      elif isinstance(people,discord.member.Member):
        pass
      else:
        await ctx.send(f"Invalid Input {people}.")
        return
      await a.set_permissions(people, read_messages=True,send_messages=True)
      data['players'][str(people.id)]['incc'].append(a.id)
      plist+="<@{}> \n".format(people.id)
    print(a.id)
    msg = await a.send("This is a new cc made by {} :- \n Participants:- \n {}".format(author.mention,plist))
    data['chnls'][str(a.id)]={}
    data['chnls'][str(a.id)]['owner']=ctx.author.id
    data['players'][str(ctx.author.id)]['incc'].append(a.id)
    await msg.pin()
    await ctx.message.delete()
    await ctx.send("Channel created.")
    dump()

@bot.command(aliases=["add"])
@commands.has_role("Alive")
async def addinchannel(ctx,member:typing.Union[discord.Member,str]):
    '''Adds a person to the channel'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    guildd=ctx.message.guild
    if member in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(member)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      member = discord.utils.get(guildd.members,id=int(idd))
    elif isinstance(member,discord.member.Member):
      pass
    else:
      await ctx.send("Invalid User")
      return
    if data['players'][str(member.id)]['state']==0:
        await ctx.send("You add a dead person to the cc.")
        return
    if ctx.author==member:
      await ctx.send("You can't add or remove yourself.")
      return
    chnl = ctx.channel.id
    guildd = ctx.message.guild
    role = discord.utils.get(guildd.roles, name="Helpers")
    if role in ctx.author.roles or data['chnls'][str(chnl)]['owner'] == ctx.author.id :
        await ctx.channel.set_permissions(member, read_messages=True,send_messages=True)
        data['players'][str(member.id)]['incc'].append(chnl)
        await ctx.send("Welcome , {} !".format(member.mention))
    else:
        await ctx.send("You probably aren't the owner of this cc.")
        
@bot.command(aliases=["remove"])
@commands.has_role("Alive")
async def removeinchannel(ctx,member:typing.Union[discord.Member,str]):
    '''Removes a person from the channel'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    guildd=ctx.message.guild
    if member in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(member)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      member = discord.utils.get(guildd.members,id=int(idd))
    elif isinstance(member,discord.member.Member):
      pass
    else:
      await ctx.send("Invalid User")
      return
    if ctx.author==member:
      await ctx.send("You can't add or remove yourself.")
      return
    chnl = ctx.channel.id
    guildd = ctx.message.guild
    role = discord.utils.get(guildd.roles, name="Helpers")
    if role in ctx.author.roles or data['chnls'][str(chnl)]['owner'] == ctx.author.id:
        await ctx.channel.set_permissions(member, read_messages=False,send_messages=False)
        data['players'][str(member.id)]['incc'].remove(chnl)
        await ctx.send("Removed {} from the cc.".format(member.mention))
    else:
        await ctx.send("You probably aren't the owner of this cc.")

@bot.command(aliases=["rename"])
@commands.has_role("Alive")
async def renamechannel(ctx,*,newname):
    '''Adds a person to the channel'''
    if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
    if newname=="battlefield" or newname=="respawning":
      await ctx.send("You cannot name a cc that.")
      return
    chnl = ctx.channel.id
    guildd = ctx.message.guild
    role = discord.utils.get(guildd.roles, name="Helpers")
    if role in ctx.author.roles  or data['chnls'][str(chnl)]['owner'] == ctx.author.id:
      try:
        await ctx.channel.edit(name=newname)
        await ctx.send("Renamed the channel to {}!".format(newname))
      except:
        await ctx.send("That did not work due to rate-limitations or some other error.")
    else:
        await ctx.send("You probably aren't the owner of this cc.")


@bot.command(aliases=["sm"])
@commands.has_role("Alive")
async def sendmoney(ctx,member:typing.Union[discord.Member,str],cash):
  '''Allows alive players to send money to others.'''
  ath=str(ctx.message.author.id)
  if (int(gamestate) != 3):
        await ctx.send("There is no game going on.")
        return
  guildd=ctx.message.guild
  if member in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(member)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      member = discord.utils.get(guildd.members,id=int(idd))
  elif isinstance(member,discord.member.Member):
      pass
  else:
      await ctx.send("Invalid User")
      return
  if int(cash) < 0:
    await ctx.send("You cannot send negative money.")
    return
  if data['money'][ath] < int(cash):
    await ctx.send("You do not have that many coins in your account.")
    return
  if data['players'][str(member.id)]['state']==0:
    await ctx.send("You send money to a dead person.")
    return
  data['money'][ath]-=int(cash)
  per=str(member.id)
  data['money'][per]+=int(cash)
  await ctx.send("Done. Sent {} to {} from {}'s account.".format(cash,member.mention,ctx.author.mention))

@bot.command(aliases=["al","alive"])
async def alivelist(ctx):
  '''Shows all alive players.'''
  if int(gamestate) != 3:
    await ctx.send("There is no game going on right now.")
    return
  guildd=bot.get_guild(448888674944548874)
  temp = ""
  temp+="All alive players are- \n"
  al=0
  for member in data['players']:
    if data['players'][member]['state']==1:
      person = discord.utils.get(guildd.members,id=int(member))
      temp +=f"{data['signedup'][member]['emoji']} - <@{member}> ({person.name}) \n"
      al+=1
  temp+="The number of alive players is- {} \n".format(al)
  msg = await ctx.send("​")
  await msg.edit(content=temp)

@bot.command(aliases=["ael"])
async def alivenonteamlist(ctx):
  '''Shows all alive players who are not on your team.'''
  if int(gamestate) != 3:
    await ctx.send("There is no game going on right now.")
    return
  guildd=bot.get_guild(448888674944548874)
  if str(ctx.message.channel.category)!=str(data['code']['gamecode']) + ' factions':
    await ctx.send("You can only use this command in faction channels.")
    return
  temp = ""
  temp+="All alive players are- \n"
  al=0
  for member in data['players']:
    if data['players'][member]['state']==1:
      if data['players'][member]['team']!=data['players'][str(ctx.author.id)]['team']:
        person = discord.utils.get(guildd.members,id=int(member))
        temp +=f"{data['signedup'][member]['emoji']} - <@{member}> ({person.name}) \n"
        al+=1
  temp+="The number of alive players is- {} \n".format(al)
  msg = await ctx.send("​")
  await msg.edit(content=temp)

@bot.command(aliases=["b"])
@commands.has_role("Alive")
async def bid(ctx,cash:int=0):
  '''Allows the person to bid in the auction. Typing 0 bids 100 more than the current bid.'''
  global data
  ath=str(ctx.author.id)
  if int(gamestate) != 3:
    await ctx.send("There is no game going on right now.")
    return
  print(ctx.message.channel)
  if data['auction']['state']==0:
    await ctx.send("There is no auction going on right now.")
    return

  await ctx.message.delete()
  team=data['players'][ath]['team']
  vaultcash=data['building'][team]['vault']
  if cash==0:
    cash=data['auction']['bid']+100
  if cash>vaultcash:
    await ctx.send("You can only bid what you have in your vault.")
    return
  leftmoney=data['building'][team]['vault']-data['building'][team]['stash']['smoney']
  if cash>leftmoney:
    await ctx.send("The cash you've tried to bid with is more that what you hold in your vault, after subtracting your tribute and/or previous bidding costs. Wait for someone to outbid you for the cash to be accessible again.")
    return
  if cash < data['auction']['bid']+100:
    await ctx.send("The current bid is higher than what you're currently offering or the increment you are making is less than 100. (You can only make increments of 100, or more.)")
    return

  oldbidder=data['auction']['bider']
  
  if oldbidder != "":
    oldbid=data['auction']['bid']
    oldteam=data['players'][oldbidder]['team']
    data['building'][oldteam]['stash']['smoney']-=oldbid
    
  data['auction']['bid']=cash
  who = f"{data['players'][ath]['team']} team"

  #who=str(ctx.author.id)
  data['auction']['bider']=str(ctx.author.id)
  data['auction']['bidern']=who
  data['building'][team]['stash']['smoney']+=cash
  guildd=bot.get_guild(448888674944548874)
  channel=bot.get_channel(int(data['auction']['chn']))
  msgid = int(data['auction']['msg'])
  msg = await channel.fetch_message(msgid)
  await msg.edit(content="Current bid - {} by {}".format(cash,who.capitalize()))
  await ctx.send("Bid Placed.")
  dump()

@bot.command(aliases=["bb","bbid"])
@commands.has_role("Alive")
async def blindbid(ctx,code,cash:int):
  '''Allows the person to put a in blind bid for the blind auction item.'''
  global data
  ath=str(ctx.author.id)
  if int(gamestate) != 3:
    await ctx.send("There is no game going on right now.")
    return
  print(ctx.message.channel)
  if code not in data['bauction']:
    await ctx.send("Invalid Code.")
    return
  await ctx.message.delete()
  if cash<=0:
    await ctx.send("Cash has to be positive.")
    return
  team=data['players'][ath]['team']
  vaultcash=data['building'][team]['vault']
  if cash>vaultcash:
    await ctx.send("You can only bid what you have in your vault.")
    return

  try:
    oldbid=data['bauction'][code]['biders'][who]
  except:
    #no old bid
    oldbid=0
  leftmoney=data['building'][team]['vault']-data['building'][team]['stash']['smoney']+oldbid
  if cash>leftmoney:
    await ctx.send("The cash you've tried to bid with is more that what you hold in your vault, after subtracting your tribute and/or previous bidding costs.")
    return

  if cash<data['bauction'][code]['minvalue']:
    await ctx.send("You need to bid more than the minimum value")
    return
  who=team
  if who in data['bauction'][code]['biders']:
    data['building'][team]['stash']['smoney']-=data['bauction'][code]['biders'][who]
  data['bauction'][code]['biders'][who]=cash
  data['building'][team]['stash']['smoney']+=cash
  await ctx.send("Done.")
  dump()

@bot.command(aliases=["ai"])
async def auctioninfo(ctx):
  '''Use this to get info on auction items'''
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  if data['auction']['state']==0:
    await ctx.send("There is no auction going on right now.")
    return
  info = discord.Embed(colour=random.randint(0, 0xffffff))
  info.set_author(name="Auction Info-")
  info.add_field(name="Item Name-",value=f"**{data['auction']['item']}**",inline="false")
  info.add_field(name="Item Perks-",value=data['auction']['perks'],inline="false")
  info.add_field(name="Current bid-",value=f"{data['auction']['bid']} by {data['auction']['bidern']}",inline="false")
  await ctx.send(embed=info)

@bot.command(aliases=["bai"])
async def blindauctioninfo(ctx,code):
  '''Use this to get info on blind auction items'''
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  if code not in data['bauction']:
    await ctx.send("Invalid Code.")
    return
  team=team=data['players'][str(ctx.author.id)]['team']
  info = discord.Embed(colour=random.randint(0, 0xffffff))
  info.set_author(name="Auction Info-")
  info.add_field(name="Item Name-",value=f"**{data['bauction'][code]['item']}**",inline="false")
  info.add_field(name="Item Perks-",value=data['bauction'][code]['perks'],inline="false")
  info.add_field(name="Min Value-",value=data['bauction'][code]['minvalue'],inline="false")
  if str(ctx.message.channel.category) == str(data['code']['gamecode']) + ' factions':
    try:
      value=data['bauction'][code]['biders'][team]
    except:
      value=0
    info.add_field(name="Your bid -",value=value,inline="false") 
  else:
    pass
  await ctx.send(embed=info)

@bot.command(aliases=["de","dep"])
@commands.has_role("Alive")
async def deposit(ctx,cash:int=0):
  '''Helps you to deposit cash to your team's vault. Typing 0 deposits your entire balance.'''
  global data
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  if str(ctx.message.channel.category)!=str(data['code']['gamecode']) + ' factions':
    await ctx.send("You can only use this command in faction channels.")
    return
  if cash<0:
    await ctx.send("Cash can't be a negative value")
    return
  ath=str(ctx.author.id)
  if cash==0:
    cash=data['money'][ath]
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
  await ctx.send(f"Done! Money transferred. {cash} was deposited.")
  dump()

@bot.command(aliases=["forcedep","fdep"])
@commands.has_role("Alive")
async def forcedeposit(ctx,person:typing.Union[discord.Member,str],cash:int=0):
  '''Allows the king of a team to force a teammate to deposit cash.'''
  global data
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  guildd=ctx.message.guild
  if person in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(person)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      person = discord.utils.get(guildd.members,id=int(idd))
  elif isinstance(person,discord.member.Member):
      pass
  else:
      await ctx.send("Invalid User")
      return
  if str(ctx.message.channel.category)!=str(data['code']['gamecode']) + ' factions':
    await ctx.send("You can only use this command in faction channels.")
    return
  if data['players'][str(person.id)]['state']==0:
        await ctx.send("You can't force a dead person to deposit.")
        return
  ath=str(ctx.author.id)
  ath2=str(person.id)
  if cash==0:
    cash=data['money'][ath2]
  if cash<0:
    await ctx.send("Cash can't be a negative value")
    return
  team=data['players'][ath]['team']
  team2=data['players'][ath2]['team']
  role = data['players'][ath]['role']
  rolet=data['rt'][role]['lirole']
  if rolet!="king" and rolet!="prince": 
    await ctx.send("You are not a king or a prince. Please only use this command if your role is King or a prince.")
    return
  if team!=team2:
    await ctx.send("That person is not on your team.")
    return
  if cash>data['money'][ath2]:
    await ctx.send("That person does not have that much cash.")
    return
  data['building'][team]['vault']+=cash
  data['money'][ath2]-=cash
  await ctx.send(f"Done! Money transferred. {cash} was deposited from {person.mention}'s account.")
  dump()

@bot.command(aliases=["w"])
@commands.has_role("Alive")
async def withdraw(ctx,cash:int):
  '''Helps you to withdraw cash from your team's vault'''
  global data
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  if str(ctx.message.channel.category)!=str(data['code']['gamecode']) + ' factions':
    await ctx.send("You can only use this command in faction channels.")
    return
  if cash<0:
    await ctx.send("Cash can't be a negative value")
    return
  ath=str(ctx.author.id)
  team=data['players'][ath]['team']
  if cash>data['building'][team]['vault']:
    await ctx.send("Your vault doesn't hold this much cash.")
    return
  leftmoney=data['building'][team]['vault']-data['building'][team]['stash']['smoney']
  if cash>leftmoney:
    await ctx.send("The cash you've requested is more that what you hold in your vault, after subtracting your tribute and bidding costs.")
    return
  data['building'][team]['vault']-=cash
  data['money'][ath]+=cash
  await ctx.send(f"Done! Money transferred. {cash} was withdrawn.")
  dump()

@bot.command(aliases=["va"])
@commands.has_role("Alive")
async def vault(ctx):
  '''Displays the amount of cash in your team's vault'''
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  if str(ctx.message.channel.category)!=str(data['code']['gamecode']) + ' factions':
    await ctx.send("You can only use this command in faction channels.")
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
  if str(ctx.message.channel.category)!=str(data['code']['gamecode']) + ' factions':
    await ctx.send("You can only use this command in faction channels.")
    return
  ath=str(ctx.author.id)

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
  if str(ctx.message.channel.category)!=str(data['code']['gamecode']) + ' factions':
    await ctx.send("You can only use this command in faction channels.")
    return
  ath=str(ctx.author.id)
  team=str(data['players'][ath]['team'])
  forglvl=data['building'][team]['forge']
  cost=int((forglvl*forglvl)*100)
  if data['money'][ath]<cost:
    await ctx.send("You cannot afford this upgrade.")
    return
  data['money'][ath]-=cost
  team=data['players'][ath]['team']
  data['building'][team]['forge']+=1
  await ctx.send("Upgrade successful.")
  dump()

@bot.command(aliases=["sinv"])
async def stockinventory(ctx):
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

@bot.command(aliases=["sbuy","by"])
async def smbuy(ctx,thing,num:int=1):
  '''Use this to buy any stocks.'''
  if int(gamestate)!=3:
    await ctx.send("There is no game going on right now.")
    return
  if data['smarket']['state']==0:
    await ctx.send("Market is closed.")
    return
  if num<0:
    await ctx.send("Number cannot be negative .")
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
async def smsell(ctx,thing,num:int=1):
  '''Use this to sell stocks.'''
  if int(gamestate)!=3:
    await ctx.send("There is no game going on right now.")
    return
  if data['smarket']['state']==0:
    await ctx.send("Market is closed.")
    return
  if num<0:
    await ctx.send("Number cannot be negative .")
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
      await ctx.send("You can only sell what you have.")
    else:
      data['money'][ath]+=cost
      data['smarket']['inv'][ath]['sun']-=num
      data['smarket']['trades']['sun']-=num
      await ctx.send("Transaction complete, you earned {}. Check your inventory.".format(cost))
  elif thing == "😏" or thing ==2:
    cost=data['smarket']['stocks']['smirk']*num
    if (data['smarket']['inv'][ath]['smirk'] - num)<0:
      await ctx.send("You can only sell what you have.")
    else:
      data['money'][ath]+=cost
      data['smarket']['inv'][ath]['smirk']-=num
      data['smarket']['trades']['smirk']-=num
      await ctx.send("Transaction complete, you earned {}. Check your inventory.".format(cost))
  elif thing == "😃" or thing ==3:
    cost=data['smarket']['stocks']['smile']*num
    if (data['smarket']['inv'][ath]['smile'] - num)<0:
      await ctx.send("You can only sell what you have.")
    else:
      data['money'][ath]+=cost
      data['smarket']['inv'][ath]['smile']-=num
      data['smarket']['trades']['smile']-=num
      await ctx.send("Transaction complete, you earned {}. Check your inventory.".format(cost))
  elif thing == "😂" or thing ==4:
    cost=data['smarket']['stocks']['joy']*num
    if (data['smarket']['inv'][ath]['joy'] - num)<0:
      await ctx.send("You can only sell what you have.")
    else:
      data['money'][ath]+=cost
      data['smarket']['inv'][ath]['joy']-=num
      data['smarket']['trades']['joy']-=num
      await ctx.send("Transaction complete, you earned {}. Check your inventory.".format(cost))
  elif thing == "😔" or thing ==5:
    cost=data['smarket']['stocks']['pens']*num
    if (data['smarket']['inv'][ath]['pens'] - num)<0:
      await ctx.send("You can only sell what you have.")
    else:
      data['money'][ath]+=cost
      data['smarket']['inv'][ath]['pens']-=num
      data['smarket']['trades']['pens']-=num
      await ctx.send("Transaction complete, you earned {}. Check your inventory.".format(cost))
  else:
    await ctx.send("Invalid stock id.")
  dump()

@bot.command(aliases=["pri"])
async def price(ctx):
  '''Use this to see the price of all stocks.'''
  if data['smarket']['state']==0:
    await ctx.send("The market it closed right now.")
    return
  a=data['smarket']['stocks']['sun']
  b=data['smarket']['stocks']['smirk']
  c=data['smarket']['stocks']['smile']
  d=data['smarket']['stocks']['joy']
  e=data['smarket']['stocks']['pens']
  await ctx.send("Cost of :sunglasses: is {} \nCost of :smirk: is {} \nCost of :smiley: is {} \nCost of :joy: is {} \nCost of :pensive: is {} \n".format(a,b,c,d,e))

@bot.command(aliases=["alert","notifyme","notif"])
async def pingme(ctx):
    '''Use this command if you want to be pinged each time the stock market values change.'''
    if int(gamestate)!=3:
      await ctx.send("There is no game going on right now.")
      return
    ath=str(ctx.author.id)
    if ath not in data['marketalert']:
      await ctx.send("You will now be notified each time the market changes.")
      data['marketalert'].append(ath)
    else:
      await ctx.send("You will no longer be notified each time the market changes.")
      data['marketalert'].remove(ath)

@bot.command(aliases=["gf","flip"])
@commands.has_role("Respawning")
async def gflip(ctx,cash:int,call):
  '''Allows the user to gamble a amount of money with a 50% chance to double it. <Respawning>'''
  global data
  if int(gamestate)!=3:
      await ctx.send("There is no game going on right now.")
      return
  if cash<0:
    await ctx.send("Number cannot be negative .")
    return
  if cash>1000:
    await ctx.send("You cannot gamble over 1000c.") #change
    return
  ath=str(ctx.author.id)
  if cash>data['money'][ath]:
    await ctx.send("You can only gamble what you have.")
    return
  flip=["head","tail"]
  if call=="h" or call=="heads":
    call="head"
  if call=="t" or call=="tails":
    call="tail"
  if call not in flip:
    await ctx.send("Call can only be \"head\" or \"tail\" or \"h\" or \"t\".")
    return
  daflip=random.choice(flip)
  if daflip==call:
    await ctx.send("Congrats! It landed {}s! You have won! {} was added to your account.".format(daflip,cash))
    data['money'][ath]+=cash
  else:
    await ctx.send("Oops! It landed {}s! {} was removed from your account.".format(daflip,cash))
    data['money'][ath]-=cash
  dump()

@bot.command(aliases=["smac","slot","slots"])
@commands.has_role("Respawning")
async def slotmachine(ctx,cash:int):
  '''Allows the user to gamble a amount in a slot machine with a chance to x10 their bet.<Respawning>'''
  global data
  if int(gamestate)!=3:
      await ctx.send("There is no game going on right now.")
      return
  if cash<0:
    await ctx.send("Number cannot be negative .")
    return
  if cash>1000:
    await ctx.send("You cannot gamble over 1000c.") #change
    return
  ath=str(ctx.author.id)
  if cash>data['money'][ath]:
    await ctx.send("You can only gamble what you have.")
    return
  flip=[':one:',':two:',':three:',':four:',':five:']
  a=random.choice(flip)
  b=random.choice(flip)
  c=random.choice(flip)
  await ctx.send("{}{}{}".format(a,b,c))
  if a==b and b==c:
    add=cash*10
    await ctx.send("Congrats! You have won {}.".format(add))
    data['money'][ath]+=add
  elif a==b or b==c or c==a:
    await ctx.send("No money was lost.".format(cash))
  else:
    data['money'][ath]-=cash
    await ctx.send("Better luck next time! {} has been removed from your account.".format(cash))
  dump()

#rip roulette
@bot.command(aliases=["die","dice"])
@commands.has_role("Respawning")
async def dicerolls(ctx,cash:int,dicen:int):
  '''Use this to play dice. Input number of dice after cash. If the total of all the dice is more than 4*number of dice , you will win cash x(the number you go over) of the cash you bet.<Respawning>'''
  global data
  if int(gamestate)!=3:
      await ctx.send("There is no game going on right now.")
      return
  if cash<0:
    await ctx.send("Number cannot be negative .")
    return
  if cash>1000:
    await ctx.send("You cannot gamble over 1000c.") #change
    return
  if dicen>100:
    await ctx.send("Dice number cannot be over 100.") #change
    return
  ath=str(ctx.author.id)
  if cash>data['money'][ath]:
    await ctx.send("You can only gamble what you have.")
    return
  die=[1,2,3,4,5,6]
  summ=0
  for a in range(dicen):
    summ+=random.choice(die)
  winno=4*dicen
  if summ>winno:
    point=summ-winno
    add=point*cash
    await ctx.send("Congrats! You have won! You got {} which was more than {}! {} has been added to your account.".format(summ,winno,add))
    data['money'][ath]+=add
  else:
    await ctx.send("Oh no! You got {} which is not more than {}! {} was deducted from your account".format(summ,winno,cash))
    data['money'][ath]-=cash
  dump()

@bot.command(aliases=["lottery","jl"])
@commands.has_role("Respawning")
async def joinlottery(ctx,tickets=1):
  '''Use this command to enter the lottery. This costs 50 coins.
  
  The prize pool increases by 500 each phase, and increases by 50 on each failed attempt. The amount in the prize pool is not visible. 
  
  You have a 1% chance of winning. If you win, you get the entire prize pool and the pool is set to 0 for everyone. 
  
  Type a number after jl (Like !jl 5) to buy multiple tickets at once. <Respawning>'''
  global data
  if int(gamestate)!=3:
      await ctx.send("There is no game going on right now.")
      return
  ath=str(ctx.author.id)
  for x in range(tickets):
    if 50>data['money'][ath]:
      await ctx.send("You need atleast 50 coins to join the lottery.")
      return
    data['money'][ath]-=50
    n = random.randint(1,101)
    if n ==49:
      await ctx.send(f"Congrats! You have won {data['lottery']} coins, {ctx.author.mention}!")
      data['money'][ath]+=data['lottery']
      data['lottery']=0
    else:
      await ctx.send("Oops, you didn't win!")
      data['lottery']+=50
  dump()


@bot.command(aliases=["mark"])
@commands.has_role("Alive")
async def market(ctx):
  '''Use this to display market.'''
  if int(gamestate)!=3:
      await ctx.send("There is no game going on right now.")
      return
  if str(ctx.message.channel.category)!=str(data['code']['gamecode']) + ' factions':
    await ctx.send("You can only use this command in faction channels.")
    return
  ath=str(ctx.author.id)
  team=data['players'][ath]['team']
  state=data['building'][team]['market']
  msg="__**MARKET**__\n"
  #if state==0:
    #msg+="You have not unlocked the market yet. Use !upmarket to unlock it for 2.5k"
  #if state>0:
  msg+=f"\n__**LVL 1 (Free)**__ \n **1.Poison someone -** They die in 2 phases if they don't buy antidode.(End phase) (Also note that posion does not stack, poisoning someone while they are already poisoned will have no additional effects. Poison can also bypass protection.) This item can only be used when the phase is about to end (the 2 phases start when the phase changes.) *- For {data['building'][team]['marketprices'][1]}* \n **2.Antidote -** Use this to cure yourself if you're poisoned. *- For {data['building'][team]['marketprices'][2]}* \n **3.Check Bal -** Use this to check one person/one team's balance/value once respectively. *- For {data['building'][team]['marketprices'][3]}* \n"
  #if state>1:
  msg+=f"\n__**LVL 2 (1k)**__ \n **4.Protection -** Use this to protect someone from all attacks for one night. *- For {data['building'][team]['marketprices'][4]}*\n **5.Respawn stone -** Use this to respawn instantly once (Only works if you are in the respawning state). *- For {data['building'][team]['marketprices'][5]}* \n **6.Respawn Totem -** Allows you to respawn once even if your king is dead. (Solos cannot buy this.) *- For {data['building'][team]['marketprices'][6]}* \n"
  #if state>2:
  msg+=f"\n__**LVL 3 (1k)**__ \n **7.Bomb -** Set a bomb in someone's house to kill them and everyone who visits them for 1 night. *- For {data['building'][team]['marketprices'][7]}* \n **8.Role Seeker -** Get the role and team of a person once and role block them for the next night. *- For {data['building'][team]['marketprices'][8]}* \n **9.Strength Potion -** Use this to make 1 of your attacks pass through any form of protection for 1 night. *- For {data['building'][team]['marketprices'][9]}* \n"
  msg+=f"\n__**LVL 4 (1k)**__ \n **10.GOD -** Protect all your teammates for the night and make all dead teammates alive instantly (Only if they're in the state respawning.) (This can be only bought once during the game) *- For {data['building'][team]['marketprices'][10]}* \n"
  await ctx.send(msg)

@bot.command(aliases=["dim"])
@commands.has_role("Alive")
async def dismarket(ctx):
  '''Displays your team's market level.'''
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  if str(ctx.message.channel.category)!=str(data['code']['gamecode']) + ' factions':
    await ctx.send("You can only use this command in faction channels.")
    return
  ath=str(ctx.author.id)
  team=data['players'][ath]['team']
  state=data['building'][team]['market']

  if state==0:
    text= "The next upgrade costs 2500."
  elif state==1:
    text= "The next upgrade costs 2500."
  elif state==2:
    text= "The next upgrade costs 2500."
  elif state==3:
    text= "The nest upgrade costs 1000."
  else:
    text= "Your market has been maxed out."
  await ctx.send(f"Your team's market is on level {state}.{text}")


@bot.command(aliases=["upm"])
@commands.has_role("Alive")
async def upmarket(ctx):
  '''Use this to upgrade market.'''
  if int(gamestate)!=3:
      await ctx.send("There is no game going on right now.")
      return
  ath=str(ctx.author.id)
  team=data['players'][ath]['team']
  state=data['building'][team]['market']

  if state==0:
    cost=1000
  elif state==1:
    cost=1000
  elif state==2:
    cost=1000
  elif state==3:
    cost=1000
  else:
    await ctx.send("Your market has already been fully upgraded.")
    return

  if data['money'][ath]<cost:
    await ctx.send("You cannot afford this.")
    return
  data['money'][ath]-=cost
  data['building'][team]['market']+=1
  await ctx.send("Upgraded!")

@bot.command(aliases=["tbuy"])
@commands.has_role("Alive")
async def tmbuy(ctx,num:int):
  '''Use this to buy something from the market. Use item number to buy.'''
  if int(gamestate)!=3:
      await ctx.send("There is no game going on right now.")
      return
  if num>10 or num<1:
    await ctx.send("Please enter a valid number.")
    return
  ath=str(ctx.author.id)
  team=data['players'][ath]['team']
  state=data['building'][team]['market']
  cost=data['building'][team]['marketprices'][num]
  if cost>data['money'][ath]:
    await ctx.send("You cannot afford this.")
    return
  if num==1:
    if state<1:
      await ctx.send("You need to upgrade your market to buy this item.")
      return
    item= "Poison"
  elif num==2:
    if state<1:
      await ctx.send("You need to upgrade your market to buy this item.")
      return
    item="Antidote"
  elif num==3:
    if state<1:
      await ctx.send("You need to upgrade your market to buy this item.")
      return
    item="Check Bal"
  elif num==4:
    if state<2:
      await ctx.send("You need to upgrade your market to buy this item.")
      return
    item="Protection"
  elif num==5:
    if state<2:
      await ctx.send("You need to upgrade your market to buy this item.")
      return
    item="Respawn Stone"
  elif num==6:
    if state<2:
      await ctx.send("You need to upgrade your market to buy this item.")
      return
    item="Respawn Tortem"
  elif num==7:
    if state<3:
      await ctx.send("You need to upgrade your market to buy this item.")
      return
    item="Bomb"
  elif num==8:
    if state<3:
      await ctx.send("You need to upgrade your market to buy this item.")
      return
    item="Role seeker"
  elif num==9:
    if state<3:
      await ctx.send("You need to upgrade your market to buy this item.")
      return
    item="Strength Potion"
  elif num==10:
    if state<4:
      await ctx.send("You need to upgrade your market to buy this item.")
      return
    item="GOD"
    data['building'][team]['marketprices'][num]+=95000
  data['money'][ath]-=cost
  data['building'][team]['marketprices'][num]+=1000
  data['players'][ath]['inv'].append(item)
  await ctx.send("Transaction successful.")
  dump()

@bot.command(aliases=["i","inv"])
async def inventory(ctx):
  '''Use this to check your inventory.'''
  if int(gamestate)!=3:
      await ctx.send("There is no game going on right now.")
      return
  if str(ctx.message.channel.category)!=str(data['code']['gamecode']) + ' factions':
    await ctx.send("You can only use this command in faction channels.")
    return
  ath=str(ctx.author.id)
  msg="You have-\n"
  for item in data['players'][ath]['inv']:
    msg+="{}\n".format(item)
  await ctx.send(msg)

@bot.command(aliases=["tri","tribute"])
@commands.has_role("Alive")
async def picktribute(ctx,person:typing.Union[discord.Member,str],cash:int):
  '''Allows the king of a team to pick the tribute and cash <King Only.>'''
  global data
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  if str(ctx.message.channel.category)!=str(data['code']['gamecode']) + ' factions':
    await ctx.send("You can only use this command in faction channels.")
    return
  if cash<1:
    await ctx.send("Cash can't be a negative value or 0.")
    return
  guildd=ctx.message.guild
  if person in emj.UNICODE_EMOJI["en"]:
      idd=emjtop(person)
      if idd== None:
        await ctx.send("Invalid Emoji")
        return
      person = discord.utils.get(guildd.members,id=int(idd))
  elif isinstance(person,discord.member.Member):
      pass
  else:
      await ctx.send("Invalid User")
      return
  ath=str(ctx.author.id)
  ath2=str(person.id)
  team=data['players'][ath]['team']
  team2=data['players'][ath2]['team']
  role = data['players'][ath]['role']
  rolet=data['rt'][role]['lirole']
  if rolet!="king" and rolet!="prince": 
    await ctx.send("You are not a king or a prince. Please only use this command if your role is King or a prince.")
    return
  if team!=team2:
    await ctx.send("That person is not on your team.")
    return
  if cash>data['building'][team]['vault']:
    await ctx.send("You do not have that much cash in your vault.")
    return

  try:
    oldtri=data['building'][team]['trihouse']['cash']
  except:
    #no old bid
    oldtri=0
  leftmoney=data['building'][team]['vault']-data['building'][team]['stash']['smoney']+oldtri
  if cash>leftmoney:
    await ctx.send("The cash you've tried to bid with is more that what you hold in your vault, after subtracting your tribute and/or previous bidding costs.")
    return
  
  if data['players'][ath2]['state']==0:
    await ctx.send("You cannot tribute a dead person.")
    return
  data['building'][team]['trihouse']['who']=ath2
  if data['building'][team]['trihouse']['cash']!=0:
    data['building'][team]['stash']['smoney']-=data['building'][team]['trihouse']['cash']
  data['building'][team]['stash']['smoney']+=cash
  data['building'][team]['trihouse']['cash']=cash
  await ctx.send(f"Done! {person.mention} was set as your tribute person and {cash} is set as your price.")

@bot.command(aliases=["store"])
@commands.has_role("Alive")
async def storeinstash(ctx,item:str):
  '''Use this to store items in your team stash <Alive>'''
  global data
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  ath=str(ctx.author.id)
  team=data['players'][ath]['team']
  try:
    data['players'][ath]['inv'].remove(item)
  except ValueError:
    await ctx.send("That item was not found in your inventory.")
    return
  data['building'][team]['stash']['items'].append(item)
  await ctx.send("Done! Item stored.")
  dump()

@bot.command(aliases=["take"])
@commands.has_role("Alive")
async def removefromstash(ctx,item:str):
  '''Use this to take items from your team stash <Alive>'''
  global data
  if int(gamestate)!=3:
    await ctx.send("There is no game going on.")
    return
  ath=str(ctx.author.id)
  team=data['players'][ath]['team']
  try:
    data['building'][team]['stash']['items'].remove(item)
  except ValueError:
    await ctx.send("That item was not found in your stash.")
    return
  data['players'][ath]['inv'].append(item)
  await ctx.send("Done! Item taken.")
  dump()

@bot.command(aliases=["stash"])
@commands.has_role("Alive")
async def viewstash(ctx):
  '''Use this to view items in your team vault <Alive>'''
  if int(gamestate)!=3:
      await ctx.send("There is no game going on right now.")
      return
  if str(ctx.message.channel.category)!=str(data['code']['gamecode']) + ' factions':
    await ctx.send("You can only use this command in faction channels.")
    return
  ath=str(ctx.author.id)
  team=data['players'][ath]['team']
  msg="You have, in your team stash-\n"
  for item in data['building'][team]['stash']['items']:
    msg+="{}\n".format(item)
  await ctx.send(msg)

@bot.command(aliases=["r"])
async def role(ctx,*,role="l"):
    '''Returns role info. '''
    await rolehelp(role,ctx)

async def rolehelp(role,chnl):
    if role == "king" or role == "1":
          msg="""```1. King-
- Is the leader of the team. Has no abilities.
- The team will stop respawning after the king's death. Chooses a person from the team for tribute , every morning. 
- Doesn't respawn.```"""
    elif role == "alert warrior" or role =="2":
        msg="""```2. Alert Warrior-
- Has the ability to go alert during the night.
- Any person attacking the alert warrior when they're alert will result in the death of the attacker.
- Action is instant. Has a cooldown of 1 day.
- Respawns in 4 phases.```"""
    elif role == "camo warrior" or role =="3" :
        msg="""```3. Camo Warrior-
- Has the ability to go camo during the night. They can either pick to go camo themselves, or pick another person to go camo instead of them. They cannot pick the same person twice in a row.
- The person cannot be killed when they have the camo mode on. (Except with the use of poison)
- Action is immediate. Has a cooldown of 1 day.
- Respawns in 4 phases.```"""
    elif role == "chief warrior" or role =="4" :
        msg="""```4. Chief Warrior-
- Chooses 1 person to kill every night.
- Kill happens at night end. Has no cooldown.
- Respawns in 2 phases on the first death , then 4 phases ever after.```"""
    elif role == "ex warrior" or role =="5" :
        msg="""```5. Ex-Warrior-
- This role is allowed to kill 1 person during the game at any time. This kill bypasses any and all forms of protection.
- Kill is instant, can be used even during day, cannot be used if dead. This ability can only be used once after which it cannot be used again. 
- Respawns in 2 phases.```"""
    elif role == "strong warrior" or role =="6" :
        msg="""```6. Strong Warrior-
- This role does not die the first night they get attacked after respawning. This ability resets after they respawn.
- They have no other abilities.
- Respawns in 6 phases.```"""
    elif role == "warrior" or role =="7" :
        msg="""```7. Warrior-
- Has no powers.
- Respawns in 2 phases.```"""
    elif role == "assassin" or role =="8" :
        msg="""```8. Assassin-
- Has the ability to kill a person every night until they lose this ability.
- The assassin will lose their ability to kill after they have died at least once.
- Kill happens during night end. No cooldown.
- Respawns in 2 phases.```"""
    elif role == "barricader" or role =="9" :
        msg="""```9. Barricader - 
- The barricader can protect people with 3 types of shield. 
-- The Divine Shield, protects the person for a night, and reveals the name of the attacker if they are attacked.
-- The Strong Shield, protects the person for a night, and has no special effects.
-- The Weak Shield, protects the person for a night, but kills you as well if the person is attacked.
- Each of the shields can be used only once, regardless of if the person is attacked or not. Gets back all the shields if they die and respawn.
- Cannot use more than 1 shield every night. Can be role blocked. Protection is instant.
- Respawns in 6 phases.```"""
    elif role == "bomber" or role =="10":
        msg="""```10. Bomber
- The bomber, when ever killed by a member of another faction, kills a certain number people of their choice.
- The bomber can pick Total people/5, rounded down, targets to kill at any point after the start of the game, and cannot change these targets at any time. They can take their time in deciding their targets, but once picked, it cannot be changed.
- If the Bomber is ever killed by a member of another faction, all the other people they have chosen will die immediately. These kills are not counted as a visit.
- The bombed can pick new targets once they have died and come back to life. The bomber dying because of tribute will not trigger their ability.
- Picking a target is immediate, and the targets are killed at the same time as when the bomber is killed.
- Respawns in 6 phases.```"""
    elif role == "builder" or role =="11" :
        msg="""```11. Builder-
- The builder gets building parts when any opponents die. Each person killed by their team gives them 2 pieces, any non team kills from outside the team gives him 1 piece. The builder can then use these parts to build the structures given below:
-- Wall - 12 parts - Protects all members of their team from all attacks for a night. Structure will remain if not attacked.
-- Fort - 21 parts - Protects all members of their team from all attacks for 2 nights. Structure will remain if not attacked.
-- Spikes - 7 parts - The builder can choose to add spiked to any already existing structures, which will kill the first attacker who tries to attack the structure. Note that spikes do not stop the structure from breaking. The attacks will still break the structures. Any kills using the spiked do not award any parts.
- The builder continues to get parts even when dead. However, they can only build when alive. Structures take 1 night to get built and only get built after the attacks occur. Two structures cannot exist at once.
- Respawns in 6 phases.```"""
    elif role == "chief knight" or role =="12":
        msg="""```12. Chief Knight
- Has the ability to kill a person every night.
- Kill is night end, and has no cooldown.
- Respawns in 6 phases.```"""
    elif role == "curse caster" or role =="13" :
        msg="""```13. Curse Caster-
- Has the ability to cast a curse on someone every night. A curse resets all prayer progress on the chosen person. 
- If the selected person is being protected by 2 prayers, it will take 2 curses to undo the protection.
- Curse casting is instant. The target is informed about what happened. Has no cooldown on abilities.
- Respawns in 4 phases.```"""
    elif role == "death swapper" or role =="14" :
        msg="""```14. Death Swapper-
- Has the ability to make anyone respawn instantly for the cost of killing themselves. 
- Action is instant. 
- Respawns in 4 phases.```"""
    elif role == "demolitionist" or role =="15" :
        msg="""```15. Demolitionist -
- Can visit someone and place a bomb in their house every night. This bomb will explode only if someone visits the target that night. The bomb will kill the person and everyone visiting.
- Placing the bomb is end night before kills and thus instant actions aren't affected but kills are.
- Respawns in 6 phases.```"""
    elif role == "disabler" or role =="16" :
        msg="""```16. Disabler-
- Can role-block a person for 1 night. Target is informed they were role-blocked.
- Has a cool down of 1 day. Picks action during the day for the following night.
- Respawns in 6 phases.```"""
    elif role == "desguiser" or role =="17" :
        msg="""```17. Disguiser-
- Has the ability to make anyone appear as any other role to all checks. 
- The targeted person is informed if they were disguised, but are not told what they are disguised as. Any applied disguises will stay until the person is killed.
- Action is instant. No cooldown.
- Respawns in 4 phases.```"""
    elif role == "finisher" or role =="18" :
        msg="""```18. Finisher-
- Can delay a person's respawn by 4 phases.
- Has a ability cooldown of 1 day. Action is night end after kills. Chooses the action during the night.
- Respawns in 6 phases.```"""
    elif role == "guard" or role =="19" :
        msg="""```19. Guard-
- Can protect someone from all attacks at all times. They will die instead of the person they protect. 
- Cannot change their target after initially picking it (Unless target somehow dies before guard). Protecting is immediate. 
- The guard cannot be role-blocked. The guard is the last layer of protection, any other protection comes first in effect before this.
- Respawns in 4 phases.```"""
    elif role == "healer" or role =="20" :
        msg="""```20. Healer-
- Can reduce a person's respawn by 4 phases.
- Has a ability cooldown of 1 day. Action is end phase after kills. Chooses the action during the night.
- Respawns in 6 phases.```"""
    elif role == "jailor" or role =="21":
        msg="""```21. Jailor
- Can pick a person every day end to imprison, for 2 phases.
- Any jailed person is protected from all attacks, is role blocked for that duration, and cannot be tributed by the team. The person is informed they were jailed.
- The jailor cannot jail the same person twice in a row.
- Action is phase end (Day end). Has no cooldown. Cannot jail themselves.
- Respawns in 6 phases.```"""
    elif role == "life transferrer" or role =="22" :
        msg="""```22. Life Transferrer-
- Has the ability to give their life to someone else. Doing so will cause all attacks targeted at the life transferrer to fail. But any attacks towards the person with the life will affect the Transferrer as well. (Including poison, and the antidote) (If the target is poisoned, you can't cure yourself, only the target can by curing themselves.)
- Action is instant. Cannot change targets after initial pick. Picks are only done during the night.Transferring life isn't a visit.
- Respawns in 4 phases.```"""
    elif role == "magician" or role =="23" :
        msg="""```23. Magician-
- Is allowed to submit a list of up to 3 guesses consisting of people's roles or both their roles and teams. If all three guesses are correct , they will be informed. But even if one of the guesses is wrong , the rest will not be confirmed.
- Action is immediate. There is no cooldown.
- Respawns in 6 phases.
```"""
    elif role == "merchant" or role =="24" :
        msg="""```24. Merchant-
- Will get back 40% of any cash spent by their team on any auction items.
- The cash is given once the day ends. Does not receive any cash by this ability when dead.
- Respawns in 4 phases.```"""
    elif role == "minister" or role =="25" :
        msg="""```25. Minister-
- If the minister is alive when the king dies , Everyone will be able to respawn again once before losing their ability to respawn.
- Respawns in 4 phases.```"""
    elif role == "negotiator" or role =="26" :
        msg="""```26. Negotiator -
- The negotiator can pick a target at any point, and if the negotiator is attacked, the target will die instead. They cannot change the target after picking, unless the target dies before the ability is used.
- They can only do this once every life. They regain this ability on death.
- Action is immediate. The target dies at the time where the negotiator was supposed to die. Redirecting the kill makes the killer visit the target instead of visiting the negotiator. 
- Respawns in 4 phases.```"""
    elif role == "observer" or role =="27" :
        msg="""```27. Observer-
- Can get the team of a person by checking them during the night.
- Action is immediate. Has no cooldown.
- Respawns in 4 phases.```"""
    elif role == "painter" or role =="28" :
        msg="""```28. Painter-
- Can paint a person every night as a certain colour or as a certain role making any inspection roles get a fake result on checking.
- Action is immediate. Has no cooldowns.
- Respawns in 2 phases.```"""
    elif role == "potion master" or role =="29" :
        msg="""```29. Potion Master-
- Can craft any of these potions to use in the game:
-- Kill potion - Use this to kill 2 people at the end of phase.
-- Protection potion - Use this to protect someone from all attacks for a night. (Doesn't expire till attacked)
-- Revive Potion - Use this to bring back a non-permanently dead teammate back to life instantly.
- All potions take 2 days to make. The potion master does not lose progress on death. The potion will be added to a person's inventory upon completion and can be used at any time. (Even Day) 
- Respawns in 6 phases.```"""
    elif role == "priest" or role =="30" :
        msg="""```30. Priest-
- Has the ability to pray for someone (even for people outside their team) every night. Once they have prayed for someone twice/thrice , they will be protected from all attacks on them for a night. (Does not expire if not attacked)
- They need to pray only twice if there is a curse caster in the game. Else, they need to pray thrice.
- Prayer is completed instantly. Has no cooldown on abilities. Target is informed if they were prayed for.
- Respawns in 4 phases.```"""
    elif role == "prince" or role =="31" :
        msg="""```31. Prince-
- Takes the place of the king, if they are alive when the king dies.
- Has no other abilities.
- Respawns in 2 phases as a prince, cannot respawn as a king.```"""
    elif role == "protector knight" or role =="32":
        msg="""```32. Protector Knight
- Has the ability to protect a person from all attacks during the night.
- Can pick a different target every night, and cannot change the target after picking for the night. Cannot pick the same person twice in a row.
- Action is immediate, and has no cooldown.
- Respawns in 6 phases.```"""
    elif role == "rich person" or role =="33" :
        msg="""```33. Rich Person-
- If the rich person is selected as tribute, any cash used for the rich person is counted as x1.5.
- Respawns in 6 phases.```"""
    elif role == "robber" or role =="34":
        msg="""```34. Robber
- Has the ability to steal money from any individual person or any team's vault, every night.
- The robber can take some of the money present inside any 1 person's balance or 1 team's vault, by winning a game against them. Winning the game would give the robber 15%, a draw would give the robber 5%, and a loss would give the robber nothing.
- The game is played by both the robber and the target picking a choice between a Bow, Shield and a Cannon. The winning order is Bow > Cannon > Shield > Bow
- In case the robber is robbing a team vault, the team can collectively decide on a choice between themselves, collectively.
- Failure to pick a choice will make them lose 15% by default. The robber can't rob a person/team twice in a row.
- The robber picks the target (Either a Person or a Team) during the day, and the target has the entire night to decide a choice. The robber gets the money when the night comes to an end. 
- Respawns in 4 phases.```"""
    elif role == "role copier" or role =="35":
        msg="""```35. Role Copier-
- Has the ability to copy the role of any dead person.
- Once copied, the role copier can choose to use the role as long as they wish. Each night they can use the role they have copied earlier, or try to copy a new role. The role copier will know the copied role immediately but cannot use it's powers till the next night (If it's a action). 
- Copying is instant. Other conditions are ported from the copied role. The copier cannot copy their dead teammates. The role copier cannot copy the same person twice in a game. 
- Respawns in 6 phases.```"""
    elif role == "seer" or role=="36":
        msg="""```36. Seer-
- Can get the role of a person by checking them during the night.
- Action is immediate. Has a cooldown of 1 day.
- Respawns in 6 phases.```"""
    elif role == "supreme knight" or role =="37":
        msg="""```37. Supreme Knight 
- Has the abilities of both Protector Knight and Chief Knight.
- Can kill 1 person at night end, or protect a person every night (Can protect same person twice in a row), but cannot kill or protect twice in a row. 
- Kill is night end, Protection is immediate and none of the actions have a cooldown.
- Respawns in 6 phases.```"""
    elif role == "tank master" or role=="38":
        msg="""```38. Tank Master -
- The tank master owns a tank which can only kill specific people from a list every night. Each night, a new list is generated from which they can choose.
- Each time they kill someone, the number of people in the list reduces by 1. At the start, there will be [(no. of people)/5 rounded down] people. This list will not include their teammates.  The list count increases to the original number upon the tank master's death.
- Alternatively, the tank master can use their tank to protect someone once in the game as  protection till they're attacked, but consequently losing the ability to use the tank forever.
- Kill is night end. Protection is instant.
- Respawns in 6 phases.```"""
    elif role == "truth seeker" or role=="39":
        msg="""```39. Truth Seeker-
- Can get the role of anyone that is dead at the moment of checking.
- Can use ability once every night. Action is immediate. No cooldowns.
- Respawns in 4 phases.```"""
    elif role == "weapon smith" or role=="40":
        msg="""```40. Weapon Smith-
- Can craft any of these weapons to use in the game:
-- Sword - 1 day prep time - Allows a person to make x2 kills if used.
-- Spear - 2 day prep time - Allows a person to make a kill that passes through all protection.
-- Cannon - 3 day prep time - Allows a person to make x4 kills if used.
- Any made weapons will kept in the weapon smith's inventory until they use/give it on/to someone. The weapon smith will not lose progress if killed when making a weapon. But the weapon smith will lose the weapons in their inventory if killed.
- Weapons are used instantly when required. 1 person can only use 1 weapon at a time.
- Respawns in 6 phases.```"""
    elif role== "wizard" or role=="41":
        msg="""```41. Wizard-
- Can reduce or increase a person's respawn time by 2 phases during the night.
- Action is night end after kills. Has a cooldown of 1 day.
- Respawns in 6 phases.```"""
    elif role== "anarchist" or role=="42":
        msg="""```42. Anarchist - SOLO
- Can kill 2 person every night. If the anarchist kills a king, he can kill 3 people every night that follows, and if he kills another king, he can kill 4 people and so on and so forth.
- If the Anarchist is attacked, the number of kills he can perform reduces by 1, ticking to 0 and eventually -1 at which point the anarchist will die.
- Kills are phase end. The Anarchist wins when there are no more kings alive. (They need to kill all princes as well). The anarchist will lose automatically if there is only 1 team alive.
- Cannot respawn.```"""
    elif role== "cult leader" or role=="43":
        msg="""```43. Cult Leader- SOLO -
- The cult leader leads their own team that wants to end all other teams in the name of peace.
- They have the ability to add a random alive person to their team chat every night. The added person is now on the cult's team and has the same win goal as the cult leader (The cult  leader is now their new king).
- The added person will not lose their abilities and will still have access to their old team chat.
- Everyone in the cult will stop respawning if the cult leader dies. The old king is irrelevant after they join the new team.
- Can't respawn. Wins if the cult is the only team alive.```"""
    elif role== "double agent" or role=="44":
        msg="""```44. Double Agent- SOLO -
-  Appears like a warrior to any two factions. They can switch to any one fraction in the game and at that point they turn into an regular warrior. If they don't switch fast enough, and get killed before they switch, they will lose the game.
- Switching is instant. The teams will be informed of the same.
- Can't respawn before picking a side, after they switch they can respawn in 2 phases.```"""
    elif role== "evil prince" or role=="45":
        msg="""```45. Evil Prince- SOLO -
- The evil prince is actually a traitor to the team. The evil prince's goal is to just get their King killed.
- Is disguised as a regular prince in role list and all checks.
- Can't respawn but wins immediately if their team king is eliminated.```"""
    elif role== "gem trader" or role=="46":
        msg="""```46. Gem Trader- SOLO -
- Starts off the game with a certain number of gems. (Number of gems = Number of people/4 , Rounded down) Can give a gem to a person every night. If a person with a gem is attacked , the attack is cancelled. Gems are permanent protection for the holder.
- Anyone with a gem can pass it to others. If the gem trader survives 1 full day with 0 gems , they win. 
- Anyone with a gem the night prior to the gem trader winning , will die. These deaths are counted as NIGHT KILLS and not day kills. No protection can save you from this.
- Gems cannot be given to anyone with a gem (Except the gem trader).If attempted to do so, your action will fail. Holding a gem disables you from performing any actions. If you are killed by the daily tribute while holding a gem , you will be killed and the gem will be returned to the gem trader.
- The gem trader can also get rid of one of their gems by paying 5000c during night ends. Gems are given to people after attacks. The gem trader automatically loses if there is only 1 team alive.
- Cannot respawn.```"""
    elif role== "item agent" or role=="47":
        msg="""```47. Item Agent- SOLO -
- Has the ability to contact a person anonymously with a choice. The item agent can choose a disguise to show to people if they use their power against them. (This disguise does not work for any other checks) 
- The contacted person can pay 1000c for the services of the item agent, and can then choose to kill a person or to reveal a person's role and colour, (or to ignore the agent, which is free). If the target picks the item agent, the item agent will show up as the chosen disguise.
- If the contacted person has less than 200c, they will be killed instantly before day starts.
- Doesn't have a cooldown. The contacted person is given the choice during the next day. The item agent will win if they complete 5 trades without dying. They will automatically lose if there is only 1 team alive.
- Cannot respawn.```"""
    elif role== "kidnapper" or role=="48":
        msg="""```48. Kidnapper- SOLO -
- Has the ability to kidnap a person once every night, starting with night 1. Doing so will tell the person's role to the kidnapper. (The person is kidnapped when day starts)
- The kidnapped person will not be able to talk in their group chat and will not be able to perform any actions, but cannot be killed when they are kidnapped. The kidnapper gets all the money that the kidnapped person had.
- The team is informed about the person from their team that has been kidnapped. The team can choose to free their teammate by paying a ransom of 1000c. If the kidnapper is killed, all the kidnapped people are released. 
- The kidnapper wins when they have kidnapped all kings at least once. They will automatically lose if there is only 1 team alive.
- Cannot respawn.```"""
    elif role== "killer" or role=="49":
        msg="""```49. Killer- SOLO -
- Kills 1 person each night. Gets 1 heart for each kill, gets 2 hearts if they kill a solo or a king.
- Has to get at least a certain number of hearts to win. Killing the same person doesn't give any hearts. Killing a person from the same team back to back gives no hearts.
- Number of hearts they need to get is Number of players/3, rounded down. Can trade in 2 hearts for 1 night protection any time. The killer has protection until they get 2 hearts for the first time.
- The killer will automatically die if they can not possibly earn enough hearts to win. They will also lose if there is only 1 team left alive.
- Has no cooldown. Kill happens at night end. 
- Doesn't respawn.```"""
    elif role== "postman" or role=="50":
        msg="""```50. Postman - SOLO -
- Can choose to give their target a Poison package (Which kills them if they open the package) or a Kill package (Which they can use to kill 1 person that night). The target isn't informed what package they receive. The target can choose to open it or dispose it. If the package is opened, the postman cannot be killed during that night.
- Package gets delivered when day start. The target has the entire day to choose. The package will be delivered even if the postman is dead. If the package is opened, the postman gets protection for the following night.
- The postman wins if 2 of each type of package are opened before the game ends.
- Cannot respawn.```"""
    elif role== "town leader" or role=="51":
        msg="""```51. Town Leader - SOLO
- As the leader of a powerful town, you have the power to kill a person every night (End Phase action), or protect someone against all attacks for a night. (You cannot protect yourself twice in a row).
- Once you have used an action on a person other than you, you can never use an action on them again in a game.
- The town leader has to choose an action on every day that they can. Failing to do so will automatically kill them.
- The town leader submits actions during the night. Protecting a person is instant, killing a person is night end. The town leader cannot change his action, if they choose to protect a person.
- You win if you survive till the end, or if you do not have a valid target to use your power on when night starts.
- Cannot respawn.```"""
    elif role=="list" or role=="l":
        msg="""All the available roles are-
```1. king
WARRIORS-
2. alert warrior
3. camo warrior
4. chief warrior
5. ex warrior
6. strong warrior
7. warrior
POWER ROLES-
8. assassin
9. barricader
10. bomber
11. builder
12. chief knight
13. curse caster
14. death swapper 
15. demolitionist
16. disabler 
17. disguiser
18. finisher
19. guard
20. healer
21. jailor
22. life transferrer
23. magician
24. merchant
25. minister
26. negotiator
27. observer
28. painter 
29. potion master
30. priest
31. prince
32. protector knight
33. rich person
34. robber
35. role copier
36. seer
37. supreme knight
38. tank master
39. truth seeker
40. weapon smith
41. wizard
SOLOS-
42. anarchist
43. cult leader
44. double agent
45. evil prince
46. gem trader 
47. item agent
48. kidnapper
49. killer
50. postman
51. town leader```"""
    else:
        msg="""Error! Role not found.Do not capitalise role names. You can also use the number (Found in #game-role-info) to represent the role.
All the available roles are-
```1. king
WARRIORS-
2. alert warrior
3. camo warrior
4. chief warrior
5. ex warrior
6. strong warrior
7. warrior
POWER ROLES-
8. assassin
9. barricader
10. bomber
11. builder
12. chief knight
13. curse caster
14. death swapper 
15. demolitionist
16. disabler 
17. disguiser
18. finisher
19. guard
20. healer
21. jailor
22. life transferrer
23. magician
24. merchant
25. minister
26. negotiator
27. observer
28. painter 
29. potion master
30. priest
31. prince
32. protector knight
33. rich person
34. robber
35. role copier
36. seer
37. supreme knight
38. tank master
39. truth seeker
40. weapon smith
41. wizard
SOLOS-
42. anarchist
43. cult leader
44. double agent
45. evil prince
46. gem trader 
47. item agent
48. kidnapper
49. killer
50. postman
51. town leader```"""
    msg = await chnl.send(msg)
    return msg

async def change():
  global data
  sun=int(random.gauss(6,18))
  smirk=int(random.gauss(4,15))
  smile=int(random.gauss(3,10))
  joy=int(random.gauss(2,7))
  pens=int(random.gauss(1,5))
  #
  data['smarket']['trades']['sun']=0
  data['smarket']['trades']['smirk']=0
  data['smarket']['trades']['smile']=0
  data['smarket']['trades']['joy']=0
  data['smarket']['trades']['pens']=0
  #
  data['smarket']['stocks']['sun']+=sun
  data['smarket']['stocks']['smirk']+=smirk
  data['smarket']['stocks']['smile']+=smile
  data['smarket']['stocks']['joy']+=joy
  data['smarket']['stocks']['pens']+=pens
  #
  if data['smarket']['stocks']['sun']<=0:
    data['smarket']['stocks']['sun']=18
  if data['smarket']['stocks']['smirk']<=0:
    data['smarket']['stocks']['smirk']=15
  if data['smarket']['stocks']['smile']<=0:
    data['smarket']['stocks']['smile']=10
  if data['smarket']['stocks']['joy']<=0:
    data['smarket']['stocks']['joy']=7
  if data['smarket']['stocks']['pens']<=0:
    data['smarket']['stocks']['pens']=5



  '''
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
#
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
#
  if data['smarket']['trades']['smile']>0:
    data['smarket']['stocks']['smile']+=10
    data['smarket']['trades']['smile']=0
  elif data['smarket']['trades']['smile']<0:
    data['smarket']['stocks']['smile']-=10
    data['smarket']['trades']['smile']=0
    if data['smarket']['stocks']['smile']<=0:
      data['smarket']['stocks']['smile']=10
  else:
    mylist=[10,0,-10]
    data['smarket']['stocks']['smile']+=random.choice(mylist)
    if data['smarket']['stocks']['smile']<=0:
      data['smarket']['stocks']['smile']=10
#
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
#
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
      data['smarket']['stocks']['pens']=5'''
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
            #data[ath])
    else:
          coins=[10,20]
          dcoins=[5,10]
          
          if not ath in earnd:
            if not str(ath) in lstmsg:
              lstmsg[str(ath)]=" "
            if lstmsg[str(ath)]==msg:
              return
            if len(msg)<10:
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

def emjtop(emj):
  for player in data['players']:
    if data['players'][player]['emoji']==emj:
      return player
  return None

def dump():
    my_collection = db.main
    my_collection.drop()
    my_collection.insert_one(data)
    '''with open('data.json', 'w+') as f:
        json.dump(data, f)'''

keep_alive.keep_alive()
bot.run(token)
  