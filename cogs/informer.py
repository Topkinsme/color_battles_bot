#a bot by top

import discord
import logging
from discord.utils import get
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Bot
import pymongo,dns,os
import asyncio
from loaddump import *

dbpass=str(os.environ.get("dbpass"))

client = pymongo.MongoClient("mongodb+srv://Topkinsme:"+dbpass+"@top-cluster.x2y8s.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test


class Test(commands.Cog):
  def __init__(self,bot):
    self.bot=bot

  @commands.Cog.listener()
  async def on_ready(self):
      await load(self.bot) 
  
  @commands.command()
  @commands.has_role("Informer")
  async def logout(self,ctx):
      '''Shuts down the bot <Informer>'''
      await ctx.send("Logging out.")
      await self.bot.logout()
      dump()
      
  @commands.command()
  @commands.has_role("Informer")
  async def purge(self,ctx,number=5):
      '''Deletes a ceratin number of messages. <Informer>'''
      chnl=ctx.channel
      await chnl.purge(limit=number+1)
      await ctx.send("Purged {} messages.".format(number))
      
  @commands.command()
  @commands.has_role("Informer")
  async def compreset(self,ctx):
      '''Complete reset. <Informer>'''
      await load(self.bot)
      global data
      global gamestate
      loaddump.data = {}
      loaddump.data['signedup']={}
      loaddump.data['gamestate']=0
      loaddump.gamestate=0
      await self.bot.change_presence(activity=discord.Game(name=" Colour battles!", type=1))
      loaddump.data['money']={}
      loaddump.data['roles']=[]
      loaddump.data['rt']={}
      loaddump.data['chnls']={}
      loaddump.data['specters']=[]
      loaddump.data['code']={}
      loaddump.data['auction']={}
      await ctx.send("A complete erasure of all data has been done.")
      dump()
      
  @commands.command()
  @commands.has_role("Informer")
  async def pdata(self,ctx):
      await load(self.bot)
      '''Send the complete data file. <Informer>'''
      print(loaddump.data)
      await ctx.send(loaddump.data)
      
  
      
  @commands.command()
  @commands.has_role("nuke")
  async def nuke(self,ctx):
      '''Empties the entire channel <Nuke>'''
      chnl=ctx.message.channel
      async for message in chnl.history(limit=10000):
          await message.delete()
      tempc = await ctx.send("Cleared.")
      await asyncio.sleep(30)
      await tempc.delete()
      
  @commands.command(aliases=["gs"])
  @commands.has_role("Informer")
  async def cgamestate(self,ctx,num):
      '''Manually changes gamestate. <Informer>'''
      await load(self.bot)
      global gamestate
      global data
      if (int(num)<0 or int(num)>4):
          await ctx.send("That is wrong. Please check the number again. Gamestate number must be always between 0 and 4.")
          return
      loaddump.gamestate=num
      loaddump.data['gamestate']=loaddump.gamestate
      print(loaddump.gamestate)
      if int(loaddump.gamestate)==1:
          await ctx.send("Signups open!")
          await self.bot.change_presence(activity=discord.Game(name="Signups open!", type=1))
      elif int(loaddump.gamestate)==2:
          await ctx.send("Signups closed!")
          await self.bot.change_presence(activity=discord.Game(name="Signups are closed.A game will soon begin.", type=1))
      elif int(loaddump.gamestate)==3:
          await ctx.send("Game has started!")
          await self.bot.change_presence(activity=discord.Game(name="Game running.", type=1))
      elif int(loaddump.gamestate)==4:
          await ctx.send("Game has concluded!")
          await self.bot.change_presence(activity=discord.Game(name="Game concluded!", type=1))
      else:
          await self.bot.change_presence(activity=discord.Game(name=" Colour battles!", type=1))
      dump()
      
  @commands.command()
  @commands.has_role("Informer")
  async def reset(self,ctx):
      '''Resets game .<Informer>'''
      await load(self.bot)
      global data
      global gamestate
      for user in loaddump.data['players']:
          guildd=self.bot.get_guild(448888674944548874)
          userr=discord.utils.get(guildd.members,id=int(user))
          role = discord.utils.get(guildd.roles, name="Spectator")
          await userr.remove_roles(role)
          role = discord.utils.get(guildd.roles, name="Dead")
          await userr.remove_roles(role)
          role = discord.utils.get(guildd.roles, name="Respawning")
          await userr.remove_roles(role)
          role = discord.utils.get(guildd.roles, name="Players")
          await userr.remove_roles(role)
      for user in loaddump.data['specters']:
          guildd=self.bot.get_guild(448888674944548874)
          userr=discord.utils.get(guildd.members,id=int(user))
          role = discord.utils.get(guildd.roles, name="Spectator")
          await userr.remove_roles(role)
      namee= loaddump.data['code']['gamecode']
      cate = discord.utils.get(ctx.message.guild.categories, name=namee)
      print(cate.channels)
      for channel in cate.channels:
          await channel.delete()
      await cate.delete()
      namee= str(loaddump.data['code']['gamecode']) + ' factions'
      cate2 = discord.utils.get(ctx.message.guild.categories, name=namee)
      print(cate2.channels)
      for channel in cate2.channels:
          await channel.delete()
      await cate2.delete()
      if loaddump.data['code']['ccno']>0:
        namee=loaddump.data['code']['gamecode'] + ' cc1'
        cate = discord.utils.get(ctx.message.guild.categories, name=namee)
        print(cate.channels)
        for channel in cate.channels:
          await channel.delete()
        await cate.delete()
      if loaddump.data['code']['ccno']>50:
        namee=loaddump.data['code']['gamecode'] + ' cc2'
        cate = discord.utils.get(ctx.message.guild.categories, name=namee)
        print(cate.channels)
        for channel in cate.channels:
          await channel.delete()
        await cate.delete()
      if loaddump.data['code']['ccno']>100:
        namee=loaddump.data['code']['gamecode'] + ' cc3'
        cate = discord.utils.get(ctx.message.guild.categories, name=namee)
        print(cate.channels)
        for channel in cate.channels:
          await channel.delete()
        await cate.delete()
      if loaddump.data['code']['ccno']>150:
        namee=loaddump.data['code']['gamecode'] + ' cc4'
        cate = discord.utils.get(ctx.message.guild.categories, name=namee)
        print(cate.channels)
        for channel in cate.channels:
          await channel.delete()
        await cate.delete()
      if loaddump.data['code']['ccno']>200:
        namee=loaddump.data['code']['gamecode'] + ' cc5'
        cate = discord.utils.get(ctx.message.guild.categories, name=namee)
        print(cate.channels)
        for channel in cate.channels:
            await channel.delete()
        await cate.delete()
      loaddump.data = {}
      loaddump.data['signedup']={}
      loaddump.data['gamestate']=0
      loaddump.gamestate=0
      await self.bot.change_presence(activity=discord.Game(name=" Colour battles!", type=1))
      loaddump.data['money']={}
      loaddump.data['roles']=[]
      loaddump.data['rt']={}
      loaddump.data['specters']=[]
      loaddump.data['players']={}
      loaddump.data['chnls']={}
      loaddump.data['code']={}
      loaddump.data['auction']={}
      dump()
      await ctx.send("Reset complete!")
      dump()

'''
async def load(bot):
      #print("Working boi!")
      global loaddump.data
      global annchannel
      global spamchannel
      global loaddump.gamestate
      global lstmsg
      spamchannel=bot.get_channel(450698253508542474)
      await spamchannel.send("The bot is online!")
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
              print("loaddump.data error")
              await spamchannel.send("Warning! loaddump.data.json wasn't found. Please check if anything is wrong.")

def dump():
    my_collection = db.main
    my_collection.drop()
    my_collection.insert_one(loaddump.data)''' '''
    with open('loaddump.data.json', 'w+') as f:
        json.dump(loaddump.data, f)'''


def setup(bot):
    bot.add_cog(Test(bot))