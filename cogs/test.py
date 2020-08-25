#a bot by top

import discord
import logging
from discord.utils import get
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Bot
import pymongo,dns,os
from cogs.roleinfo import *
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
  async def sping(self,ctx):
    '''Returns sPong.'''
    print("sPong!")
    await ctx.send("sPong!")
    #dump()

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
          data = my_collection.find_one()
          loaddump.gamestate = data['gamestate']
          '''with open('data.json','r') as f:
              data = json.load(f)
              print(data)
              loaddump.gamestate = data['gamestate']'''
      except:
              print("Could not load the data")
              data = {}
              data['signedup']={}
              data['gamestate']=0
              loaddump.gamestate=0
              data['money']={}
              data['roles']=[]
              data['rt']={}
              data['chnls']={}
              data['specters']=[]
              data['code']={}
              data['auction']={}
              dump()
              print("data error")
              await spamchannel.send("Warning! Data.json wasn't found. Please check if anything is wrong.")

def dump():
    my_collection = db.main
    my_collection.drop()
    my_collection.insert_one(data)
    '''with open('data.json', 'w+') as f:
        json.dump(data, f)'''


def setup(bot):
    bot.add_cog(Test(bot))