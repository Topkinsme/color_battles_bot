#a bot by top

import discord
import logging
from discord.utils import get
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Bot
import pymongo,dns,os
import random
from loaddump import *

dbpass=str(os.environ.get("dbpass"))

client = pymongo.MongoClient("mongodb+srv://Topkinsme:"+dbpass+"@top-cluster.x2y8s.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test

class Events(commands.Cog):
  def __init__(self,bot):
    self.bot=bot   

  @commands.Cog.listener()
  async def on_ready(self):
      await load(self.bot) 
    
  @tasks.loop(minutes=5)
  async def my_loop():
      global earnd
      global lstmsg
      earnd=[]
  my_loop.start()
                          
  @commands.Cog.listener()
  async def on_message(self,message):
      await load(self.bot)
      global gamestate
      if message.author.id == 450320950026567692:
          return
      #await self.bot.process_commands(message)
      if int(loaddump.gamestate) != 3:
          return
      ath=str(message.author.id)
      fath=message.author
      channel = message.channel
      await score(self,ath,message.content)
      #await levelup(ath,fath,channel)
      
  @commands.Cog.listener()
  async def on_command_error(self,ctx,error):
      await ctx.send(error)
      
  @commands.Cog.listener()
  async def on_member_join(self,member):
      await spamchannel.send("{} joined the server".format(member.mention))
      
  @commands.Cog.listener()
  async def on_member_remove(self,member):
      await spamchannel.send("{} left the server".format(member.mention))
      
  @commands.Cog.listener()
  async def on_message_delete(self,message):
      await spamchannel.send("'{}' was deleted in <#{}>".format(message.content,message.channel.id))
      
  @commands.Cog.listener()
  async def on_user_update(self,before,after):
      if before.name==after.name:
          return
      else:
          await spamchannel.send("'{}' has changed his name to '{}' .".format(before.name,after.name))

  @commands.Cog.listener()
  async def on_raw_reaction_add(self,payload):
      await load(self.bot)
      userid=payload.user_id
      msgid=payload.message_id
      channelid=payload.channel_id
      guildd=self.bot.get_guild(448888674944548874)
      channel=self.bot.get_channel(channelid)
      userr=discord.utils.get(guildd.members,id=userid)
      emoji=str(payload.emoji)
      msg = await channel.fetch_message(msgid)
      #print(emoji)
      role1 = discord.utils.get(guildd.roles, name="Players")
      role2 = discord.utils.get(guildd.roles, name="Respawning")
      role3 = discord.utils.get(guildd.roles, name="Dead")
      role4 = discord.utils.get(guildd.roles, name="Spectator")
      if role2 in userr.roles or role3 in userr.roles or role4 in userr.roles:
        await msg.remove_reaction(emoji,userr)
      elif role1 in userr.roles and emoji=="📌":
        await msg.pin()

  @commands.Cog.listener()
  async def on_raw_reaction_remove(self,payload):
      await load(self.bot)
      userid=payload.user_id
      msgid=payload.message_id
      channelid=payload.channel_id
      guildd=self.bot.get_guild(448888674944548874)
      channel=self.bot.get_channel(channelid)
      userr=discord.utils.get(guildd.members,id=userid)
      emoji=str(payload.emoji)
      msg = await channel.fetch_message(msgid)
      #print(emoji)
      role1 = discord.utils.get(guildd.roles, name="Players")
      role2 = discord.utils.get(guildd.roles, name="Respawning")
      role3 = discord.utils.get(guildd.roles, name="Dead")
      role4 = discord.utils.get(guildd.roles, name="Spectator")
      if role2 in userr.roles or role3 in userr.roles or role4 in userr.roles:
        return
      elif role1 in userr.roles and emoji=="📌":
        await msg.unpin()

async def score(self,ath,msg):
    await load(self.bot)
    global data
    global earnd
    global lstmsg
    if not ath in loaddump.data['money']: 
            loaddump.data['money'][ath]=0
            dump()
            #print(loaddump.data[ath])
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

                if loaddump.data['players'][ath]['state'] ==0:
                    add= random.choice(dcoins)
                    loaddump.data['money'][ath]+=int(add)
                    earnd.append(ath)
                    lstmsg[str(ath)]=msg
                else:
                  add= random.choice(coins)
                  loaddump.data['money'][ath]+=int(add)
                  earnd.append(ath)
                  lstmsg[str(ath)]=msg
              except KeyError:
                add= random.choice(coins)
                loaddump.data['money'][ath]+=int(add)
                earnd.append(ath)
                lstmsg[str(ath)]=msg
          else:
            return
          dump()
    dump()
          #print(loaddump.data[ath])
'''
async def load(bot):
      #print("Working boi!")
      global loaddump.data
      global annchannel
      global spamchannel
      global gamestate
      global lstmsg
      spamchannel=bot.get_channel(450698253508542474)
      #wait spamchannel.send("The bot is online!")
      lstmsg={}
      try:
          my_collection = db.main
          loaddump.data = my_collection.find_one()
          gamestate = loaddump.data['gamestate']''''''
          with open('loaddump.data.json','r') as f:
              loaddump.data = json.load(f)
              print(loaddump.data)
              gamestate = loaddump.data['gamestate']''''''
      except:
              print("Could not load the loaddump.data")
              loaddump.data = {}
              loaddump.data['signedup']={}
              loaddump.data['gamestate']=0
              gamestate=0
              loaddump.data['money']={}
              loaddump.data['roles']=[]
              loaddump.data['rt']={}
              loaddump.data['chnls']={}
              loaddump.data['specters']=[]
              loaddump.data['code']={}
              loaddump.data['auction']={}
              dump()
              print("loaddump.data error")
              await spamchannel.send("Warning! loaddump.data.json wasn't found. Please check if anything is wrong.")

def dump():
    my_collection = db.main
    my_collection.drop()
    my_collection.insert_one(loaddump.data)''''''
    with open('loaddump.data.json', 'w+') as f:
        json.dump(loaddump.data, f)'''


def setup(bot):
    bot.add_cog(Events(bot))