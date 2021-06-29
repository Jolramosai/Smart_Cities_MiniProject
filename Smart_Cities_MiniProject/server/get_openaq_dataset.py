import json
import datetime
import requests
import matplotlib.pyplot as plt

def get_city_pollution(date,city,max_tries=10):
    
    parameter = "o3"
    date_from = str(date)
    date_to = str(date)

    pollution = requests.get(f"https://api.openaq.org/v1/measurements?city={city}&parameter={parameter}&date_from={date_from}&date_to={date_to}")

    pollution = pollution.json()
    
    ##print(json.dumps(pollution,indent = 2))
    values = [x['value'] for x in pollution['results']]
    
    if(len(values) == 0):
        for i in range(max_tries):
            date_from = str(date - datetime.timedelta(days=i))
            pollution = requests.get(f"https://api.openaq.org/v1/measurements?city={city}&parameter={parameter}&date_from={date_from}&date_to={date_to}")
            pollution = pollution.json()
            values = [x['value'] for x in pollution['results']]
            
            if(len(values) > 0):
                break


    return sum(values)/len(values)

def get_cities_pollution(date,cities):
    pollution_values = dict()
    for city in cities:

        '''try:
            pollution_values[city] = get_city_pollution(http,date,city)
        except:
            print(f"Couldn't get pollution info for city {city}")
        '''
        pollution_values[city] = get_city_pollution(date,city)
    return pollution_values

def get_pollution_by_day(start_date,end_date,cities):
    
    pollution_by_day = dict()
    
    while start_date < end_date:
        pollution_by_day[str(start_date)] = get_cities_pollution(start_date,cities)
        start_date += datetime.timedelta(days=1)
    
    return pollution_by_day

def save_to_file(news,fname):
    with open(fname,'w') as f:
        json.dump(news,f,indent = 4)

def make_graph_pollution(citie,sources,saveloc):
    with open(sources,'r') as f:
        pollution = json.load(f)
    
    ##print([pollution[x][citie] for x in pollution])
    
    plt.plot([pollution[x][citie] for x in pollution])

    plt.ylabel("O3 levels in ug")
    plt.xlabel("days")
    plt.legend(loc="lower right")
    plt.savefig(saveloc)
    plt.close()


def get_todays_pollution(cities):

    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(days=1)

    todays_pollution = get_pollution_by_day(today,tomorrow,cities)

    return todays_pollution

def main():
    cities = ['Lisboa','Braga','Porto','Aveiro','Faro']

    ##pollution = get_pollution_by_day(datetime.date(2020,3,1),datetime.date(2020,3,29),cities)
    
    ##print(json.dumps(pollution,indent = 2))
    ##save_to_file(pollution,"o3.json")
    
    for citie in cities:
        make_graph_pollution(citie,"data/o3.json",f"imgs/{citie}.png")
    
##main()

##print(get_todays_pollution(['Braga','Porto','Lisboa','Faro','Aveiro']))
