#from extractclocation import getcarmenloc
#from hydrator import tweetshydrator
#import pandas as pd
import os
import json
import re
import string
import pickle

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

from textblob import Blobber
tb = Blobber(analyzer=NaiveBayesAnalyzer())

import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")
nltk.download('stopwords')

from nltk.corpus import stopwords

stop_words = stopwords.words('english')
#reference
#https://github.com/thepanacealab/covid19_twitter/blob/master/COVID_19_dataset_Tutorial.ipynb


percent = 0.1
#input data directory
inputdatadir = r'hydrate files sample %s%%' %(int(percent*100))
#output data directory
outputdatadir = 'sentiment files %s%%' %(int(percent*100))
if not os.path.exists(outputdatadir):
    os.makedirs(outputdatadir)

keywords = ['vaccin','vax']

from sentiment140_bayes import extract_features,trainingmodel

if os.path.exists('classifier140.pkl'):
    classifier140 = pickle.load( open('classifier140.pkl', 'rb'))
    word_features = pickle.load( open('word_features.pkl', 'rb'))
else:
    classifier140,sucratio,word_features = trainingmodel(totalsize=30000,testpct=0.9)
    pickle.dump(classifier140, open('classifier140.pkl', 'wb'))
    pickle.dump(word_features, open('word_features.pkl', 'wb'))


def findkeywords(s,keywords):
    find = False
    for k in keywords:
        if re.search(k,s) is not None:
            find = True
    return find    



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


#hydrate tweets
idfile_list = os.listdir(inputdatadir)
for idfile in idfile_list:
    print(idfile)
    if idfile.split('.')[0].endswith('carmen'):
        #input
        rawfile = os.path.join(inputdatadir,idfile)
        #output
        sentiment_file = os.path.join(outputdatadir, '{}.json'.format( idfile.split('.')[0] ))
        if not os.path.exists(sentiment_file):
            output_file = open(sentiment_file,'w')
            with open(rawfile, 'r',encoding='utf-8') as f:
                for line in f.readlines():
                    tweet = json.loads(line)
                    if (tweet['lang']=='en') & (tweet['CarmenLoc'] is not None) :
                        if (tweet['CarmenLoc']['country'].lower()=='united states') :
                            if findkeywords(tweet['full_text'],keywords):
                                text = tweet['full_text']
                                print(tweet['id'])

                                #tokens
                                tokens = TreebankWordTokenizer().tokenize(text)
                                #remove noise
                                cleaned_tokens = remove_noise(tokens, stop_words )
                                senti140 = classifier140.classify(extract_features(cleaned_tokens,word_features))
                                
                                #https://stackabuse.com/sentiment-analysis-in-python-with-textblob/
                                textblobsent1 = TextBlob(text).sentiment
                                #textblobsent = TextBlob(text,analyzer=NaiveBayesAnalyzer()).sentiment
                                textblobsent2 = tb(text).sentiment
                                #https://www.analyticsvidhya.com/blog/2021/10/sentiment-analysis-with-textblob-and-vader/
                                # VADER
                                sid_obj = SentimentIntensityAnalyzer()
                                vadersent = sid_obj.polarity_scores(text)
                                res = {'id':tweet['id'],'text':text,'senti140':str(senti140),
                                       'textblobsent1':textblobsent1,'textblobsent2':textblobsent2,
                                       'vadersent':vadersent}
                                #output file
                                json.dump(res, output_file)
                                output_file.write('\n')
                                
            output_file.close()

    
    