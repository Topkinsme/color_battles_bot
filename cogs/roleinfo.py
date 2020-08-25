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


class Roleinfo(commands.Cog):
  def __init__(self,bot):
    self.bot=bot

  @commands.Cog.listener()
  async def on_ready(self):
      await load(self.bot) 

  @commands.command(aliases=["ri"])
  async def role(self,ctx,*,role):
    '''Returns role info. '''
    await rolehelp(role,ctx)



'''async def load(bot):
      #print("Working boi!")
      global loaddump.data
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
          gamestate = loaddump.data['gamestate']
          ''''''with open('loaddump.data.json','r') as f:
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
              await spamchannel.send("Warning! loaddump.data.json wasn't found. Please check if anything is wrong.")'''

async def rolehelp(role,chnl):
    if role == "king" or role == "1":
          await chnl.send("```1. King - \n -Doesn't have any power but faction can't respawn with out him ! Kill this person to destroy the faction! \n -Can't respawn.```")
    elif role == "warrior" or role =="2":
        await chnl.send("```2.Warrior - \n -Doesn't have any powers. \n -Respawns in 1 in game days.```")
    elif role == "potion master" or role =="3" :
        await chnl.send("```3.Potion master - \n -Can choose to craft a poison potion (2 days preparation time) which can kill 2 people at once, a protection potion (2 days preparation time) which can be used to protect someone once for 1 attack, or a respawn potion (2 days preparation time) which can used to respawn a person instantly (except the king) and use it on someone or store it for future use. \n -The potion master cannot make multiple potions at once. And potions are not immediate. \n - If a potion master is killed , they will lose all potions stored , and will lose progress on any potion they were crafting. \n -Respawns in 3 days.```")
    elif role == "wizard" or role =="4" :
        await chnl.send("```4.Wizard - \n  -Can delay a person's respawn by 1 day. \n   -Respawns in 3 days.```")
    elif role == "chief warrior" or role =="5" :
        await chnl.send("```5.Chief Warrior - \n -Chooses who to kill and takes advice from other members of the faction,respawns much quicker at the start and then it  get slower. \n - Respawns in 1 day on the first death , then 2 days after.```")
    elif role == "prince" or role =="6" :
        await chnl.send("```6.Prince - \n  -Takes the place of the king , if he is alive when the king dies. \n - Respawns in a day as prince , but can't respawn as the king.```")
    elif role == "disabler" or role =="7" :
        await chnl.send("```7.Disabler - \n  -Can immobilize a person for a day, making him unable to use any powers. \n -Respawns in 3 days.```")
    elif role == "killer" or role =="8" :
        await chnl.send("```8.Killer - SOLO role \n - Is a solo role , he kills people individually once a day. Wins if he has killed at least 50% of the people in game at least once. \n  -Can't respawn```")
    elif role == "reviver" or role =="9" :
        await chnl.send("```9.Reviver - \n  - Can reduce a player's respawn time by 50 % or increase someone's respawn time by 50%. \n  - Respawns in 3 days.```")
    elif role == "camo warrior" or role =="10" :
        await chnl.send("```10.Camo warrior - \n  -This role cannot be killed when he activates camo mode. Cooldown for this ability is 2 days. \n -Respawns in 2 days.```")
    elif role == "seer" or role =="11" :
        await chnl.send("```11. Seer - \n  - Can get the role of a person, by using his ability on a person thrice. Doesn't lose progress if killed or changes target in between.\n  - Respawns in 3 days.```")
    elif role == "guard" or role =="12" :
        await chnl.send("```12.Guard - \n   - Can protect someone once every lifetime.(He will die instead of the person he protects.) Cannot change target after initially picking it. \n - Respawns in 2 days.```")
    elif role == "observer" or role =="13" :
        await chnl.send("```13.Observer - \n -Can know the color of a targeted person instantly. \n -Respawns in 2 days.```")
    elif role == "painter" or role =="14" :
        await chnl.send("```14. Painter - \n  -Can paint a person to make his allegiance appear as something else to checks. \n -Respawns in 2 days.```")
    elif role == "builder" or role =="15" :
        await chnl.send("```15.Builder -  \n  - Building materials can be found when any opponent is killed. Each person killed by his team gives him 2 pieces. \n  -Once 8 pieces has been acquired , the builder can build a wall. This wall will stop any attacks towards his team for a night. The wall will not get destroyed if the team wasn't attacked \n   -Respawns in 2 day.```")
    elif role == "double agent" or role =="16" :
        await chnl.send("```16.Double agent - SOLO role - \n - Appears like a warrior to any two factions. He can switch to any one fraction in the game and at that point turns into an regular warrior .If he doesn't switch fast enough , and he gets killed , he cannot respawn  and will lose.```")
    elif role == "strong warrior" or role =="17" :
        await chnl.send("```17.Strong Warrior- \n -Needs to be attacked twice for him to die. He does not lose this ability after dying. \n   -Respawns in 3 days.```")
    elif role == "ex warrior" or role =="18" :
        await chnl.send("```18.Ex Warrior- \n -Is allowed to kill 1 person during the game at any time. (Not an immediate action. \n -Respawns in 1 days```")
    elif role == "priest" or role =="19" :
        await chnl.send("```19.Priest- \n  - Can pray for someone (even for people outside their team) every day. Once he has prayed for someone thrice , they will be protected from the next attack. \n   -Respawns in 3 days.```")
    elif role == "curse caster" or role =="20" :
        await chnl.send("```20.Curse caster- \n   -Can reset the priest's progress of prayers on someone. If someone has a complete protecting , cursing on him twice will remove the protection. Can cast a curse everyday. \n  -Respawns in 2 days.```")
    elif role == "kidnapper" or role =="21" :
        await chnl.send("```21.Kidnapper - SOLO role - \n  -Can kidnap a person once every 3 days , after night 1. \n  -Kidnapped people lose access to their chats and loses the ability to perform actions. The kidnapped person also cannot be killed during this duration. The kidnapper gets all the money that the kidnapped person had. The kidnapper is kept anonymous and can send  anonymous messages to the kidnapped person. The team can free the kidnapped person after paying a ransom of 1000c. \n   -Kidnapper cannot respawn. If the kidnapper is killed , then all kidnapped people are released. \n  -The kidnapper wins when he has kidnapped all the kings atleast once.```")
    elif role == "item agent" or role =="22" :
        await chnl.send("```22.Item Agent - SOLO role - \n -Every night he can contact a person and he gives him a choice. \n  -The contacted person can choose to kill a person or to reveal a person's role and color. ( or to ignore him) \n -If the contacted person accepts, The agent will take all his money. \n  -If the Item agent gets 2500c (By trades only.) , he wins. \n -If a person contacted has less than 500c , he will automatically die.```")
    elif role == "life transferrer" or role =="23" :
        await chnl.send("```23.Life transferrer- \n  -Can make it so that his life is transferred to another person in game. Doing so will cause all attacks towards them to fail , but if their target is attacked , they will die. \n    -Respawns in 3 days.```")
    elif role == "role stealer" or role =="24" :
        await chnl.send("```24.Role stealer- \n    -Can steal the ability of a dead person. Stolen person will be able to use ability as well. \n   -Respawns in 3 days.```")
    elif role == "death swapper" or role =="25" :
        await chnl.send("```25.Death Swapper- \n -Can make anyone respawn for the cost of killing himself. (Person respawns the next day) \n  -Respawns in 2 days```")
    elif role == "gem trader" or role =="26" :
        await chnl.send("```26.Gem trader - SOLO role \n - Starts off the game with a certain number of gems. (Number of gems = Number of people/4 , Rounded down) Can give a gem to a person every night. Anyone with a gem cannot be killed until they give it to others. \n -Anyone with a gem can pass it to others. \n -If the gem trader survives 1 full day with 0 gems , they win. Anyone with a gem the night prior to the gem trader winning , will die. These deaths are counted as NIGHT KILLS and not day kills. Any form of night protection will save you from this. (Even a guard protection.) \n -Gems cannot be given to anyone with a gem (Except the gem trader). Holding a gem disables you from performing any actions. \n -If you are killed by the daily tribute while holding a gem , you will be killed and the gem will be returned to the gem trader. \n -The gem trader can also get rid of one of his gems by paying 5000c.```")
    elif role == "disguiser" or role =="27":
        await chnl.send("```27. Disguiser - \n -Can make any person appear as any other role to all checks. \n -Respawns in 2 days.```")
    elif role == "alert warrior" or role=="28":
        await chnl.send("```28. Alert Warrior - \n -Can choose to stay awake at night , killing anyone who visits him. Cooldown for his ability is 2 days. \n -Respawns in 2 days.```")
    elif role == "assassin" or role=="29":
        await chnl.send("```29. Assassin- \n -Can kill one every night. \n -Respawns in 3 days.```")
    elif role == "merchant" or role=="30":
        await chnl.send("```30. Merchant- \n -Will get back 50% of any cash spent by his team for any market items. \n -Respawns in 2 days.```")
    elif role=="list" or role=="l":
        await chnl.send("All the available roles are- \n ``` 1.king \n 2.warrior \n 3.potion master \n 4.wizard \n 5.chief warrior \n 6.prince \n 7.disabler \n 8.killer \n 9.reviver \n 10.camo warrior \n 11.seer \n 12.guard \n 13.observer \n 14.painter \n 15.builder \n 16.double agent \n 17.strong warrior \n 18.ex warrior \n 19.priest \n 20.curse caster \n 21.kidnapper \n 22.item agent \n 23.life transferrer \n 24.role stealer \n 25.death swapper \n 26.gem trader \n 27.disguiser \n 28.alert warrior \n 29.assassin \n 30.merchant```")
    else:
        await chnl.send("Error! Role not found.No not capitalise role names. You can also use the number (Found in #role info) to represent the role.\n All the available roles are- \n ``` 1.king \n 2.warrior \n 3.potion master \n 4.wizard \n 5.chief warrior \n 6.prince \n 7.disabler \n 8.killer \n 9.reviver \n 10.camo warrior \n 11.seer \n 12.guard \n 13.observer \n 14.painter \n 15.builder \n 16.double agent \n 17.strong warrior \n 18.ex warrior \n 19.priest \n 20.curse caster \n 21.kidnapper \n 22.item agent \n 23.life transferrer \n 24.role stealer \n 25.death swapper \n 26.gem trader \n 27.disguiser \n 28.alert warrior \n 29.assassin \n 30.merchant```")
        





'''
def dump():
    my_collection = db.main
    my_collection.drop()
    my_collection.insert_one(loaddump.data)
    commentwith open('loaddump.data.json', 'w+') as f:
        json.dump(loaddump.data, f)comment
'''

def setup(bot):
    bot.add_cog(Roleinfo(bot))