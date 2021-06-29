from firebase import firebase
import json

## Get all the data from a given collection in the database
def get_data(collection):
    global db
    return db.get(collection,'')

##send data to a given collection
def send_data(collection,data):
    global db
    db.post(collection + "/",data)

##get all the values from the polluition database
def get_pollution():
    pollution = dict()
    data = get_data('pollution')
    for i in data:
        pollution[data[i]['day']] = data[i]['values'] 
    return pollution

##get the headlines from the news collection
def get_news():
    news = dict()
    data = get_data('news')
    for i in data:
        news[data[i]['day']] = data[i]['values']
    
    return news

##get the contacts list from the news contacts collection
def get_contacts():
    data = get_data("contacts")
    return [(data[i]['name'],data[i]['email']) for i in data]

##send a single date/value document to a collection
def send_value(collection,day,values):
    data = {"day": day,"values": values}
    send_data(collection,data)

def send_values(collection,dict_object):
     for i in dict_object:
         send_value(collection,i,dict_object[i])

def send_ozone_value(obj,day):
    send_value("pollution",day,obj)

def send_news_value(obj,day):
    send_value("news",day,obj)

def send_values_json(collection,json_f):
    
    with open(json_f) as f:
        print(f)
        dict_object = json.load(f)
    
    send_values(collection,dict_object)

def send_ozone_values_json(json_f):
    send_values_json("pollution",json_f)

def send_news_values_json(json_f):
    send_values_json("news",json_f)

def send_statistics(statistics):
    send_data("statistics",statistics)

def init_firebase():
    global db
    db = firebase.FirebaseApplication('https://ozone-a07ef.firebaseio.com/',None)

##init_firebase()
##send_news_values_json("data/news.json")
##send_ozone_values_json("data/o3.json")
##print(json.dumps(get_news(),indent = 2))
##print(json.dumps(get_pollution(),indent = 2))
##print(get_contacts())

##send_statistics({"win":10,"loose":100})
##send_ozone_value("2019-01-20",{"Braga":10,"Lisboa":20})
