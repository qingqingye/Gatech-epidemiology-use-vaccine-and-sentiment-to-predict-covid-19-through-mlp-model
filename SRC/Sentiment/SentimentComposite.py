import os
import json
import re
import string
from dateutil.parser import parse
import numpy as np
import pandas as pd


percent = 0.1#0.05
#input data directory
inputdatadir = r'sentiment files %s%%' %(int(percent*100))

    
#hydrate tweets
idfile_list = os.listdir(inputdatadir)
sentiment_index = []
for idfile in idfile_list:
    print(idfile)
    #input
    rawfile = os.path.join(inputdatadir,idfile)
    #date
    t = parse(os.path.basename(rawfile).split('_')[0]).date()
    senti_ = []
    with open(rawfile, 'r',encoding='utf-8') as f:
        #a = f.readlines()
        #print(len(f.readlines()))
        for line in f.readlines():  
            data = json.loads(line)
            senti_.append([data['id'],data['senti140']=='1',data['textblobsent1'][0]=='pos',
                           data['textblobsent2'][0]=='pos',data['vadersent']['compound']>0        ])
    senti_ = np.array(senti_) 
    sentiidx = (senti_[:,1:].sum(axis=0)/senti_.shape[0]).tolist()
    sentiment_index.append([t]+sentiidx+[senti_.shape[0]])
#sentiment
sentiment_df = pd.DataFrame(sentiment_index,columns=['date','sentiment140','textblob1','textblob2','vader','n'])
sentiment_df = sentiment_df.sort_values(by='date')

corr= sentiment_df[['sentiment140','textblob2','vader','n']].corr()

sentiindex = sentiment_df[['date','sentiment140','textblob2','vader','n']]
sentiindex.to_csv('SentimentIndex %s%%.csv' %(int(percent*100)),encoding='utf-8',index=False)

