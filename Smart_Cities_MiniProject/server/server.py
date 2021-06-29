import time
from get_news_dataset import get_todays_news
import datetime
import models
from realtime_database import init_firebase,send_statistics,get_news,get_pollution
import prepare_data
from get_openaq_dataset import get_todays_pollution
import numpy as np
import json
import matplotlib.pyplot as plt
from sendmail import sendmails


def create_statistics_graph(pollution,saveloc):
    values = [pollution[x] for x in pollution]
    labels = [x for x in pollution]
    
    x = np.arange(len(labels))
    
    plt.subplots(figsize=(17,5))
    plt.bar(x,values)

    plt.xticks(x,tuple(labels))
    plt.savefig(saveloc)
    plt.close()

def get_trained_model(architecture,cities,max_days=30,ngram_size=2):

    news = get_news()
    pollution = get_pollution()
    days = [(x,pollution[x]) for x in pollution]
    days = sorted(days,key=lambda x:datetime.datetime.strptime(x[0], '%Y-%m-%d'))
    
    last30days = dict()

    for x in cities:
        last30days[x] = [str(i[1][x]) for i in days[:max_days]]

    data,vocab,transformer = prepare_data.preprocess_data(cities,news,pollution,ngram_size)

    if(architecture == "dnn"):
        model,scaler  = models.get_model_dnn(data)
    
    elif(architecture == "lstm"):
        model,scaler  = models.get_model_lstm(data)
    
    return (model,scaler,vocab,last30days,transformer)

def get_statistics(cities,model,scaler,vocab,
                    transformer,last30days,
                    OpenAQ_KEY,keywords,
                    ngrams_statistics=5):
    
    statistics = dict()
    variations = dict()
    predicted_pollution = dict()
    common_ngrams = dict()

    todays_news = get_todays_news(OpenAQ_KEY,keywords)
    todays_news = [todays_news[i] for i in todays_news][0]

    todays_pollution = get_todays_pollution(cities)
    todays_pollution = [todays_pollution[i] for i in todays_pollution][0]

    ngram_vector = transformer(todays_news)
    print(sum(ngram_vector))
    scaled_vector = scaler.transform(np.array([ngram_vector]))
    predictions = model.predict(scaled_vector)[0]
    
    for x in range(len(cities)):
        variations[cities[x]] = str(predictions[x])
        predicted_pollution[cities[x]] = str(todays_pollution[cities[x]]*predictions[x])

    if(ngrams_statistics > len(vocab)):
        ngrams_statistics = len(vocab)

    ngrams_repetitions = [(vocab[x],ngram_vector[x]) for x in range(len(vocab))]
    ngrams_repetitions = sorted(ngrams_repetitions,key = lambda x: x[1],reverse=True)

    if(len(ngrams_repetitions) < ngrams_statistics):
        ngrams_statistics = len(ngrams_repetitions)
    
    for x in range(ngrams_statistics):
        common_ngrams[str(ngrams_repetitions[x][0])] = str(ngrams_repetitions[x][1])


    statistics["variations"] = variations
    statistics["pollution"]  = predicted_pollution
    statistics["ngrams"] = common_ngrams
    statistics["last30days"] = last30days

    return statistics


def start_server(WaitTime=120,predictions_per_mail=3,architecture="lstm"):
    
    init_firebase()
    OpenAQ_KEY = "ac5826a382134b4fa83bc68b311bf1b1"
    keywords = ["Lisbon","Braga","Porto","Aveiro","Faro","Portugal","Europa"]
    cities = ['Braga','Porto','Lisboa','Faro','Aveiro']

    email = ""
    password = ""
    
    link = "https://ozone-a07ef.firebaseapp.com/#"
    
    message = lambda x: f"""Bom dia {x} neste mail seguem os valores de ozono previstos para as diferentes cidades. 
                            Visite {link} para obter mais informação."""
    subject = "Predições de ozono"
    image_path = "imgs/statistics.png"
    todays_pollution = get_todays_pollution(cities)
    print(todays_pollution)
    starting_day = datetime.datetime.now().date()
    model,scaler,vocab,last30days,transformer = get_trained_model(architecture,cities)
    
    predictions = 0

    while(True):
        print("running") 
        
        today = datetime.datetime.now().date()

        statistics = get_statistics(cities,model,scaler,vocab,
                    transformer,last30days,
                    OpenAQ_KEY,keywords,
                    ngrams_statistics=5)
        
    
        send_statistics(statistics)
        
        if(predictions == predictions_per_mail):
            create_statistics_graph(statistics["pollution"],image_path)
            sendmails(email,password,message,subject,image_path)
            predictions = 0

        if(today > starting_day):
            starting_day = today
            model,scaler,vocab,last30days,transformer = get_trained_model(architecture,cities)
            

        predictions += 1
        time.sleep(WaitTime)

       



start_server(20)
