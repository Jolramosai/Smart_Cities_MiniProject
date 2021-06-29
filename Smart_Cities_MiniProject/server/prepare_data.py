import json
from nltk.corpus import stopwords
import re
from nltk.util import ngrams
import numpy
from datetime import datetime
from nltk.stem.lancaster import LancasterStemmer
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

def word_extraction(sentence):
    stop_words = set(stopwords.words('english'))
    st = LancasterStemmer()
    words = sentence.split()
    cleaned_text = [st.stem(w.lower()) for w in words if w not in stop_words and len(w) > 2]
    return cleaned_text
    
def tokenize(sentences,ngram_size=1,max_tokens = 256):
    _ngrams = list()
    

    for sentence in sentences:
        _ngrams.extend(ngrams(word_extraction(sentence),ngram_size))

    ngram_count = Counter(_ngrams) 
     
    tokens = sorted(ngram_count.items(),key = lambda x:x[1],reverse = True)[:max_tokens]
    
    ##return tokens

    tokens = [x[0] for x in tokens]
    ##print(tokens)
    ##print(" ")
    ##print(list(ngram_count.keys())[:max_tokens])
    ##print(tokens)
    return tokens

def bagNgramsVector(sentences,vocab,ngram_size=1):
    
    bag_vector = numpy.zeros(len(vocab))
    
    for sentence in sentences:
    
        _ngrams = list(ngrams(word_extraction(clean_sentence(sentence)),ngram_size))
        for n in _ngrams:
            for i,ng in enumerate(vocab):
                if n == ng:
                    bag_vector[i] += 1
    
    ##print(sum(bag_vector)) 
    return list(bag_vector)

def clean_sentence(sentence):
    ponctuation = r'[\_\$\€\"\-;%()|\.,+&.,!\?\:\*@\[\]\'\´\´\‘\’]'
    
    sentence = re.sub(r"[0-9]","",sentence)
    sentence = re.sub(r"(\'s|`s|´s|\‘s|\’s)"," ",sentence)
    sentence = re.sub(ponctuation,"",sentence)
    sentence = re.sub(r"\s+\w\s","",sentence)

    ##print(sentence.lower())
    return sentence.lower()
    
def preprocess_text(news,ngram_size=1):
    
    sentences = list()
    
    for i in news:
        for x in news[i]:
            sentences.append(clean_sentence(x))
    
    ##for i in sentences:
        ##print(i)

    vocab = tokenize(sentences,ngram_size)
    ##return vocab[:16]
    print(len(vocab)) 
    
    vector_dict = dict()
    
    for i in news:
        vector_dict[i] = bagNgramsVector(news[i],vocab,ngram_size)
 
    return (vector_dict,vocab)

def preprocess_pollution(pollution,cities):
    
    sorted_keys = sorted(pollution.keys(),key = lambda x: datetime.strptime(x,'%Y-%m-%d'))
    
    variations = dict()
    
    for i in range(len(sorted_keys) - 1):
        variations_i = dict()

        for x in pollution[sorted_keys[i]].keys():
            variations_i[x] = pollution[sorted_keys[i+1]][x] / pollution[sorted_keys[i]][x]
    
        variations[sorted_keys[i]] = [variations_i[x] for x in cities]
        
    return variations

def make_graph_variations(citie,variations,saveloc):

    plt.plot([variations[x][citie] for x in variations])

    plt.ylabel("variation in o3 levels absolute value")
    plt.xlabel("days")
    plt.savefig(saveloc)
    plt.close()

def make_graph_ngrams(ngrams,saveloc):
    
    values = [x[1] for x in ngrams]
    print(values)
    x = numpy.arange(len(ngrams))
    fig, ax = plt.subplots(figsize=(20,5))
    plt.bar(x,values)
    plt.ylabel("repetitions")
    plt.xticks(x,tuple([x[0] for x in ngrams]))
    plt.savefig(saveloc)
    plt.close()

def make_graph_sparse(ngrams,saveloc):
   
    print(ngrams)
    values = [sum([i for i in ngrams[x] if i != 0]) for x in ngrams]
    
    plt.plot(values,label = "free positions")
    plt.plot([256 for x in range(len(ngrams))],label= "total position")
    plt.ylabel("non zero positions in the ngram vector")
    plt.xlabel("days")
    plt.legend(loc="center right")
    plt.savefig(saveloc)
    plt.close()

def create_dataframe(text,pollution):
    data = list()
    for i in pollution: 
        if i in text:
            data.append([text[i],pollution[i]])
    
    df = pd.DataFrame(data,columns = ['headlines','variations'])
    return df

def create_csv(text,pollution,csv_file):
    df = create_dataframe(text,pollution)
    df.to_csv(csv_file)

def preprocess_data(cities,news,pollution,ngram_size=2):
    pt,vocab = preprocess_text(news,ngram_size=ngram_size)
    pp = preprocess_pollution(pollution,cities)
    text_transformer  = lambda x: bagNgramsVector(x,vocab,ngram_size=ngram_size)
    df = create_dataframe(pt,pp)
    return (df,vocab,text_transformer)

def main():
    
    global cities
    cities = ['Braga','Porto','Lisboa','Faro','Aveiro']

    ngram_size = 2

    with open('data/o3.json') as f:
        pollution = json.load(f)

    with open('data/news.json') as f:
        news = json.load(f)


    ##pt = preprocess_text(news,ngram_size=2)
    ##pd = preprocess_pollution(pollution,cities)
    
    vocab = preprocess_text(news,ngram_size=ngram_size)
    make_graph_sparse(vocab,"imgs/sparse.png")
    ##make_graph_ngrams(vocab[:8],'imgs/ngrams.png')
    ##create_csv(pt,pd,"data/TextPollution.csv")
    ##print(len(pt))
    ##for i in range(len(cities)):
        ##make_graph_variations(i,pd,f"imgs/variation_{cities[i]}.png")
##main()
