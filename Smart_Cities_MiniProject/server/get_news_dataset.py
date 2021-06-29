from newsapi import NewsApiClient
import json
import datetime
import matplotlib.pyplot as plt

def get_top_headlines(newsapi,keyword,source):
    
    top_headlines = newsapi.get_top_headlines(q=keyword)
    
    return top_headlines

def get_articles_range(newsapi,start_date,end_date,key,source):
    
    all_articles = newsapi.get_everything(q=key,sources=source,
            from_param = start_date,
            to = end_date,
            language='en',
            sort_by = "relevancy")
   
    return all_articles

def get_titles_range(newsapi,date,keys,source):
   
    all_titles = list()
    
    for keyword in keys:
        articles = get_articles_range(newsapi,str(date),str(date),keyword,source)
        titles = [x['title'] for x in articles['articles']]
        all_titles.extend(titles)
    
    return all_titles

def get_titles_by_day(api_key,start_date,end_date,keys):
    
    newsapi = NewsApiClient(api_key = api_key)
    
    sources = newsapi.get_sources()

    sources = [x['id'] for x in sources['sources']]
    
    titles_by_day = dict()
    source = ",".join(sources)

    while start_date < end_date:
        titles_by_day[str(start_date)] = get_titles_range(newsapi,start_date,keys,source)
        start_date += datetime.timedelta(days=1)
    
    return titles_by_day

def save_to_file(news,fname):
    with open(fname,'w') as f:
        json.dump(news,f,indent = 4)

def make_graph_number_articles(sources,saveloc):
    with open(sources,'r') as f:
        news = json.load(f)
    
    print([len(news[x]) for x in news])

    plt.plot([len(news[x]) for x in news])

    plt.ylabel("number of articles")
    plt.xlabel("days")
    plt.legend(loc="lower right")
    plt.savefig(saveloc)

def get_todays_news(API_KEY,keywords):
    
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(days=1)
    print(today)
    todays_titles = get_titles_by_day(API_KEY,today,tomorrow,keywords)
    return todays_titles

def main():
    API_KEY = "ac5826a382134b4fa83bc68b311bf1b1"
    keywords = ["Lisbon","Braga","Porto","Aveiro","Faro","Portugal","Europa"]
    
    print(datetime.date(2020,3,1))
    print(get_todays_news(API_KEY,keywords))
    ##make_graph_number_articles('data/news.json','imgs/number_articles.png')
    titles_by_day = get_titles_by_day(API_KEY,datetime.date(2020,3,28),datetime.date(2020,3,29),keywords)
    print(titles_by_day)
    ##save_to_file(titles_by_day,"news.json")
    ##print(json.dumps(titles_by_day,indent = 2))
    
##main()
