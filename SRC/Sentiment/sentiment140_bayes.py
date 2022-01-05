import numpy as np
import pandas as pd
import re
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import string
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import TreebankWordTokenizer

stop_words = stopwords.words('english')


def process_text(text):
    hashtags = re.compile(r"^#\S+|\s#\S+")
    mentions = re.compile(r"^@\S+|\s@\S+")
    text = re.sub(r'http\S+', '', text)
    text = hashtags.sub(' hashtag', text)
    text = mentions.sub(' entity', text)
    return text.strip().lower()


def remove_noise(tweet_tokens, stop_words ):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def extract_features(document,word_features):
    document_words = set(document)
    features = {}
    for word in word_features:
       features['contains(%s)' % word] = (word in document_words)
    return features


def importdata():
    #import data
    df = pd.read_csv(r'sentiment140\training.1600000.processed.noemoticon.csv', encoding='latin-1', header = None)
    df.columns=['Sentiment', 'id', 'Date', 'Query', 'User', 'Tweet']
    df = df.drop(columns=['id', 'Date', 'Query', 'User'], axis=1)
    df['Sentiment'] = df.Sentiment.replace(4,1)
    df['Tweet'] = df.Tweet.apply(process_text)
    
    
    labels = df.Sentiment.values
    text = df.Tweet.values
    return labels,text

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features


def trainingmodel(totalsize=1000,testpct=0.8):
    labels,text = importdata()
    
    tweets = []
    randomi = np.random.choice(list(range(labels.shape[0])),size=totalsize,replace=False)
    for i in randomi:
        t = text[i]
        #tokens
        tokens = TreebankWordTokenizer().tokenize(t)
        #remove noise
        cleaned_tokens = remove_noise(tokens, stop_words )
        tweets.append((cleaned_tokens,labels[i]))
    
    #word features
    word_features = list(get_word_features(get_words_in_tweets(tweets)))
    
    #training
    randomtrain = np.random.choice(list(range(len(randomi))),size=int(len(randomi)*0.8),replace=False)
    training_tweets = [tweets[x ] for x in randomtrain]
    
    training_set = nltk.classify.apply_features(lambda x:extract_features(x,word_features),training_tweets)
    classifier140 = nltk.NaiveBayesClassifier.train(training_set)
    
    test_tweets = [tweets[x] for x in set(list(range(len(randomi)))).difference(randomtrain)]
    suc = 0
    for i in test_tweets:
        if classifier140.classify(extract_features(i[0],word_features))==i[1]:
           suc += 1 
    sucratio = suc/len(test_tweets)
    return classifier140,sucratio,word_features



"""
from textblob import TextBlob 
from textblob.sentiments import NaiveBayesAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
test_text = [(text[randomi[x]],labels[randomi[x]]) for x in set(list(range(len(randomi)))).difference(randomtrain)]

suc2 = 0
suc3 = 0
sid_obj = SentimentIntensityAnalyzer()
for t,l in test_text:
    textblobsent = TextBlob(i,analyzer=NaiveBayesAnalyzer()).sentiment
    if ((textblobsent.classification=='pos') & (l==1)) | ((textblobsent.classification=='neg') & (l==0)):
        suc2 += 1
    
    vadersent = sid_obj.polarity_scores(t)
    if ((vadersent['compound']>0) & (l==1)) | ((vadersent['compound']<0) & (l==0)) :
        suc3 += 1
"""    

