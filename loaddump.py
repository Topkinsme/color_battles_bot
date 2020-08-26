#code by top

import pymongo,dns,os


dbpass=str(os.environ.get("dbpass"))

client = pymongo.MongoClient("mongodb+srv://Topkinsme:"+dbpass+"@top-cluster.x2y8s.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test

data={}
gamestate=0
spamchannel=""

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
          gamestate = data['gamestate']
          '''
          with open('data.json','r') as f:
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
              dump()
              print("data error")
              await spamchannel.send("Warning! Data.json wasn't found. Please check if anything is wrong.")

def dump():
    my_collection = db.main
    my_collection.drop()
    my_collection.insert_one(data)
    '''with open('data.json', 'w+') as f:
        json.dump(data, f)'''