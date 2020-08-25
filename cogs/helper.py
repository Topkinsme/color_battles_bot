#a bot by top

import discord
import logging
from discord.utils import get
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Bot
import pymongo,dns,os
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
  @commands.has_role("Helpers")
  async def poll(self,ctx,*,message):
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

  @commands.command()
  @commands.has_role("Helpers")
  async def kick(self,ctx,member:discord.Member):
      '''To kick a person out of the server. <Helper>'''
      await member.kick()
      await ctx.send("{} has been kicked from the server.".format(member.mention))

  @commands.command()
  @commands.has_role("Helpers")
  async def ban(self,ctx,member:discord.Member):
      '''To ban a person from the server. <Helper>'''
      await member.ban()
      await ctx.send("{} has been banned from the server.".format(member.mention))
      
  @commands.command(aliases=["rc"])
  @commands.has_role("Helpers")
  async def removecash(self,ctx,member:discord.Member,cash):
      '''Removes a certain amount of cash from a person. <Helper>'''
      await load(self.bot)
      if (int(loaddump.gamestate) != 3):
          await ctx.send("There is no game going on.")
          return
      loaddump.data['money'][str(member.id)]-=int(cash)
      await ctx.send("{} has been reduced from {}'s account. Current balance is {} .".format(cash,member.mention,loaddump.data['money'][str(member.id)]))
      dump()
      
  @commands.command(aliases=["ac"])
  @commands.has_role("Helpers")
  async def addcash(self,ctx,member:discord.Member,cash):
      '''Adds a certain amount of cash to a person's balance. <Helper>'''
      await load(self.bot)
      if (int(loaddump.gamestate) != 3):
          await ctx.send("There is no game going on.")
          return
      loaddump.data['money'][str(member.id)]+=int(cash)
      await ctx.send("{} has been added to {}'s account. Current balance is {} .".format(cash,member.mention,loaddump.data['money'][str(member.id)]))
      dump()
      
  @commands.command(aliases=["gso"])
  @commands.has_role("Helpers")
  async def opensignups(self,ctx):
      '''Opens signups. <Helpers>'''
      await load(self.bot)
      global gamestate
      loaddump.gamestate = 1
      loaddump.data['gamestate']=loaddump.gamestate
      sgchannel=self.bot.get_channel(739400216146477137)
      guildd=ctx.message.guild
      role0 = discord.utils.get(guildd.roles, name="Helpers")
      await sgchannel.set_permissions(guildd.default_role, read_messages=True,send_messages=True)
      await sgchannel.set_permissions(role0, read_messages=True,send_messages=True)
      await ctx.send("Signups open!")
      await self.bot.change_presence(activity=discord.Game(name="Signups open!", type=1))
      dump()
      
  @commands.command(aliases=["gsc"])
  @commands.has_role("Helpers")
  async def closesignups(self,ctx):
      '''Closes signups. <Helpers>'''
      await load(self.bot)
      global gamestate
      loaddump.gamestate = 2
      loaddump.data['gamestate']=loaddump.gamestate
      sgchannel=self.bot.get_channel(739400216146477137)
      guildd=ctx.message.guild
      role0 = discord.utils.get(guildd.roles, name="Helpers")
      await sgchannel.set_permissions(guildd.default_role,read_messages=True,send_messages=False)
      await sgchannel.set_permissions(role0, read_messages=True,send_messages=True)
      await ctx.send("Signups closed!")
      await self.bot.change_presence(activity=discord.Game(name="Signups are closed.A game will soon begin.", type=1))
      dump()
  


'''
async def load(bot):
      #print("Working boi!")
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
          loaddump.data = my_collection.find_one()
          gamestate = loaddump.data['gamestate']''' ''''
          with open('loaddump.data.json','r') as f:
              loaddump.data = json.load(f)
              print(loaddump.data)
              gamestate = loaddump.data['gamestate']''' '''
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
    my_collection.insert_one(loaddump.data)''' '''
    with open('loaddump.data.json', 'w+') as f:
        json.dump(loaddump.data, f)'''


def setup(bot):
    bot.add_cog(Test(bot))