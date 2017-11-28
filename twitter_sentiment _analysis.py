import re
from collections import defaultdict, Counter
import yaml
import Algorithmia
from textblob import TextBlob
import requests
import json
client = Algorithmia.client("simW9KNxC87AhVZALH+6v/L+dk31")

def text_processing():
    
    tweet_list=[]
    tweet_data=[]
    with open("output.txt") as f:
        data = f.read().splitlines()
    for line in data:
        try:
            tweet=yaml.load(line)
            tweet_data.append(tweet)
        except:
            continue

    for tweet in tweet_data:
        try:
            data=tweet['text']
            tweet_list.append(data)
        except:
            continue
    
    regex_remove = "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^RT|http.+?"
    stripped_text = [
        re.sub(regex_remove, '',tweets).strip() for tweets in tweet_list
    ]
    #print('. '.join(stripped_text))
    return '. '.join(stripped_text)

def data_processing():
    
    tweet_list=[]
    tweet_data=[]
    with open("output.txt") as f:
        data = f.read().splitlines()
    for line in data:
        try:
            tweet=yaml.load(line)
            tweet_data.append(tweet)
        except:
            continue

    for tweet in tweet_data:
        try:
            data=tweet['text']
            tweet_list.append(data)
        except:
            continue
    
    regex_remove = "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^RT|http.+?"
    stripped_text = [
        re.sub(regex_remove, '',tweets).strip() for tweets in tweet_list
    ]
    return stripped_text

def named_entity():
    
    data = text_processing()
    ne_algo = client.algo('StanfordNLP/NamedEntityRecognition/0.1.1').set_options(timeout=600)
    ne_result = ne_algo.pipe(data).result
##    file=open("result.txt","w")
##    for line in ne_result:
##        print(line)
##    file.close()
    return ne_result



def data_grouping():
    data = named_entity()
    default_dict = defaultdict(list)
    for items in data:
        for k, v in items:
            if 'LOCATION' in v or 'ORGANIZATION' in v or 'PERSON' in v or 'NAME' in v or 'PRODUCT' in v:
                default_dict[v].append(k.upper())
    ne_list = [{keys: Counter(values)}
                for (keys, values) in default_dict.items()]    
    return ne_list


def get_top_five():
    lis=data_grouping()
    dict_data={}
    for i in lis:
        for k,v in i.items():
            for key,val in v.items():
                dict_data[key]=val
    list_result=[]
    i=5
    dict_data_sorted_keys=sorted(dict_data, key=dict_data.get, reverse=True)
    for key in dict_data_sorted_keys:
        list_result.append(key)
        i-=1
        if i==0:
            break
        
    return list_result

def sentiment_analysis(all_news):
    sentiment_topic=[]
    #all_tweets = get_news()
    for line in all_news:
        try:
            sentiment_news = {}
            sentiment_news['text']=line
            analysis = TextBlob(line)
            if analysis.sentiment.polarity > 0:
                sentiment_news['sentiment']='positive'
                #print ('positive')
            elif analysis.sentiment.polarity == 0:
                sentiment_news['sentiment']='neutral'
                #print ('neutral')
            else:
                sentiment_news['sentiment']='negative'
                #print ('negative')
            sentiment_topic.append(sentiment_news)
        except:
            continue
    #print(sentiment_topic)
    return sentiment_topic

def get_news(entity_object):
  
        news_description=[]
        url = ('https://newsapi.org/v2/everything?'
           'q=%s&'
           'from=2017-11-25&'
           'sortBy=popularity&'
           'apiKey=8c7827349c4a41aaaedeb9012d720a5b'% entity_object)

        response = requests.get(url)
        json_object=json.loads(response.text)
        for i in range (0, len (json_object['articles'])):
            #print (json_object['articles'][i]['description'])
            news_description.append(json_object['articles'][i]['description'])
        output = sentiment_analysis(news_description)
        return output
#print (response.json)

def extract_tweet(substr,data):
    tweet_list=[]
    for line in data:
        caps_line=line.upper()
        if caps_line.find(substr)>=0:
            tweet_list.append(line)       
    return tweet_list

def main():
    list_entity = get_top_five()
    data = data_processing()
    temp_list=[]
    twt_list=[]
    print("News Analysis")
    for entity in list_entity:
        print(entity)
        tweets=get_news(entity)
        #print(tweets)
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        print("Positive news percentage:{} %".format(100*len(ptweets)/len(tweets)))
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        print("Negative news percentage: {} %".format(100*len(ntweets)/len(tweets)))
        print("Neutral news percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
        temp_list = extract_tweet(entity,data)
        twt_list.append(temp_list)
    i=0
    print("\n\nTweet Analysis")
    for tweet in twt_list:
        print(list_entity[i])
        i+=1
        tweets_analysis=sentiment_analysis(tweet)
        ##print(tweets)
        ptweets = [tweet for tweet in tweets_analysis if tweet['sentiment'] == 'positive']
        print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets_analysis)))
        ntweets = [tweet for tweet in tweets_analysis if tweet['sentiment'] == 'negative']
        print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets_analysis)))
        print("Neutral tweets percentage: {} %".format(100*(len(tweets_analysis) - len(ntweets) - len(ptweets))/len(tweets_analysis)))
        
if __name__ == '__main__':
    main()
    

    
