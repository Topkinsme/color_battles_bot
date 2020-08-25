#a bot by top

import discord
import logging
from discord.utils import get
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Bot
import pymongo,dns,os
from cogs.roleinfo import *
from cogs.helper import *
import random
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

  @commands.command(aliases=["s"])
  @commands.has_role("Helpers")
  async def start(self,ctx,code:str,num=0):
    '''Starts the game (Type a number after s to run the assignroles command automatically) <Helpers>'''
    await load(self.bot)
    global gamestate
    global data
    if int(loaddump.gamestate)!=2:
        await ctx.send("Check the gamestate.")
        return
    if loaddump.data['roles'] == []:
        await ctx.send("Role list is empty....")
        return
    loaddump.gamestate=3
    loaddump.data['gamestate']=loaddump.gamestate
    loaddump.data['code']['gamecode']=str(code)
    await ctx.send("Game has started with code {} !".format(code))
    await self.bot.change_presence(activity=discord.Game(name="Game running.", type=1))
    loaddump.data['players']={}
    loaddump.data['code']['ccno']=0
    for user in loaddump.data['signedup']:
        loaddump.data['players'][user]={}
        loaddump.data['players'][user]['incc']=[]
        guildd=self.bot.get_guild(448888674944548874)
        userr=discord.utils.get(guildd.members,id=int(user))
        role = discord.utils.get(guildd.roles, name="Signed-Up!")
        await userr.remove_roles(role)
        guildd=self.bot.get_guild(448888674944548874)
        role = discord.utils.get(guildd.roles, name="Players")
        await userr.add_roles(role)
    dump()
    if num !=0:
        await assignroles(self,ctx,code)
    dump()
        
  @commands.command(aliases=["as"])
  @commands.has_role("Helpers")
  async def assignroles(self,ctx,code):
    '''Assigns roles and makes all channels. <Helpers>'''
    await load(self.bot)
    global data
    if int(loaddump.gamestate) != 3:
        await ctx.send("The game hasn't started")
        return
    listoplayers = []
    rolelist=[]
    #
    guildd=ctx.message.guild
    role0 = discord.utils.get(guildd.roles, name="Helpers") 
    role1 = discord.utils.get(guildd.roles, name="Players")
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
    town = {
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
    namee = str(loaddump.data['code']['gamecode'])
    await guildd.create_category(namee)
    cate = discord.utils.get(ctx.message.guild.categories, name=namee)
    story = await guildd.create_text_channel('story-time',overwrites=storymark,category=cate)
    global townc
    townc = await guildd.create_text_channel('townhall',overwrites=town,category=cate)
    markc = await guildd.create_text_channel('market',overwrites=storymark,category=cate)
    respc = await guildd.create_text_channel('respawning',overwrites=resp,category=cate)      
    deadsc = await guildd.create_text_channel('dead-spec',overwrites=deads,category=cate) 
    await townc.send("Welcome to this city, my fellow citizens! \n This is our townhall , where we disscuss the topic important about our city.Feel free to introduce yourselves!")
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
    namee = str(loaddump.data['code']['gamecode'])+' factions'
    await guildd.create_category(namee)
    cate = discord.utils.get(ctx.message.guild.categories, name=namee)
    red = await guildd.create_text_channel('red',overwrites=overwrites,category=cate)
    blue = await guildd.create_text_channel('blue',overwrites=overwrites,category=cate)
    green = await guildd.create_text_channel('green',overwrites=overwrites,category=cate)
    yellow = await guildd.create_text_channel('yellow',overwrites=overwrites,category=cate)
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
    for player in loaddump.data['players']:
          listoplayers.append(player)
          #print(listoplayers)
    for role in loaddump.data['roles']:
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
          loaddump.data['players'][user]['role']=role
          loaddump.data['players'][user]['team']=loaddump.data['rt'][role]['team']
          loaddump.data['players'][user]['state']=1
          #state 1 is alive ,0 is dead
          #print(loaddump.data)
          num+=1
    #print(loaddump.data)
    #
    for user in loaddump.data['players']:
          guildd=self.bot.get_guild(448888674944548874)
          userr=discord.utils.get(guildd.members,id=int(user))
          roleinfo=discord.Embed(colour=discord.Colour.red())
          roleinfo.set_author(name="Role info!")
          roleinfo.add_field(name="This message has been sent to you to inform you of the role you have in the next up coming game in the Colour Battles server!",value="**Your role for this game is `{}` and you are in the team `{}`!** \n You are **__not__** allowed to share this message! \n You are **__not__** allowed to share the screenshot of this message! \n Breaking any of these rules can result in you being banned from the server.".format(loaddump.data['players'][user]['role'],loaddump.data['players'][user]['team']),inline="false")
          roleinfo.add_field(name="If you need help reagrding this role or this game , please make sure to contact the Informers or the Helpers or read the role info from from the #role_info channel.",value="Have a good game!\n *I am a bot and this action has been done automatically. Please contact the informer is anything is unclear.* ",inline="false")
          await userr.send(embed=roleinfo)
          if loaddump.data['players'][user]['team']=="red":
              await red.set_permissions(userr, read_messages=True,send_messages=True,add_reactions=True)
              loaddump.data['players'][str(user)]['incc'].append(red.id)
          elif loaddump.data['players'][user]['team']=="blue":
              await blue.set_permissions(userr, read_messages=True,send_messages=True,add_reactions=True)
              loaddump.data['players'][str(user)]['incc'].append(blue.id)
          elif loaddump.data['players'][user]['team']=="green":
              await green.set_permissions(userr, read_messages=True,send_messages=True,add_reactions=True)
              loaddump.data['players'][str(user)]['incc'].append(green.id)
          elif loaddump.data['players'][user]['team']=="yellow":
              await yellow.set_permissions(userr, read_messages=True,send_messages=True,add_reactions=True)
              loaddump.data['players'][str(user)]['incc'].append(yellow.id)
          roleid= loaddump.data['players'][user]['role']
          rolename=loaddump.data['rt'][roleid]['lirole']
          chnlname = str(loaddump.data['players'][user]['team']) + "_" + str(rolename)
          chnl = await guildd.create_text_channel(chnlname,overwrites=overwrites,category=cate)
          await chnl.set_permissions(userr, read_messages=True,send_messages=True)
          role = loaddump.data['players'][user]['role']
          rolet=loaddump.data['rt'][role]['lirole']
          await rolehelp(rolet,chnl)
          #loaddump.data['players'][str(user)]['incc'].append(chnl.id) THIS DISABLES PEOPLE FROM TALKING IN CHAT WHEN DEAD
    dump()
    await listallr(ctx)
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