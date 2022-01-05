# Developed during Biomedical Hackathon 6 - http://blah6.linkedannotation.org/
# Authors: Ramya Tekumalla, Javad Asl, Juan M. Banda
# Contributors: Kevin B. Cohen, Joanthan Lucero

import sys
import tweepy
import json
import math
#import glob
#import csv
#import zipfile
#import zlib
import os
import os.path as osp
import pandas as pd
from time import sleep
import numpy as np



def tweetshydrator(inputfile,outputfile,keyfile,percent=0.1,hydration_mode='e'):
    """
    hydrate Tweets data
    
    reference:
    https://github.com/thepanacealab/SMMT/tree/master/data_acquisition\get_metadata.py    
    
    """
    with open(keyfile) as f:
        keys = json.load(f)
     
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True, retry_delay=60*3, retry_count=5,retry_errors=set([401, 404, 500, 503]), )
    
    if api.verify_credentials() == False: 
        print("Your twitter api credentials are invalid") 
        sys.exit()
    else: 
        print("Your twitter api credentials are valid.") 
    
    output_file = outputfile

    output_file_noformat = output_file.split(".",maxsplit=1)[0]
    output_file = '{}'.format(output_file)
    output_file_log = '{}_log.txt'.format(output_file_noformat)   
    
    if '.tsv' in inputfile:
        inputfile_data = pd.read_csv(inputfile, sep='\t')
        #print('tab seperated file, using \\t delimiter')
    elif '.csv' in inputfile:
        inputfile_data = pd.read_csv(inputfile)
    elif '.txt' in inputfile:
        inputfile_data = pd.read_csv(inputfile, sep='\n', header=None, names= ['tweet_id'] )
        #print(inputfile_data)
    
    #filter
    inputfile_data = inputfile_data[(inputfile_data['lang']=='en')].set_index('tweet_id')
    #random sample 
    ntotal = inputfile_data.shape[0]
    randomchoose = np.random.choice(list(range(ntotal)),int(np.ceil(ntotal*percent)))
        
    #ids
    ids = list(inputfile_data.iloc[randomchoose,:].index)
    print('total ids: %s , sample ids: %s' %(inputfile_data.shape[0],len(ids)))

    start = 0
    end = 100
    limit = len(ids)
    i = int(math.ceil(float(limit) / 100))

    last_tweet = None
    if osp.isfile(outputfile) and osp.getsize(outputfile) > 0:
        with open(output_file, 'rb') as f:
            #may be a large file, seeking without iterating
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
            last_line = f.readline().decode()
        last_tweet = json.loads(last_line)
        start = ids.index(last_tweet['id'])
        end = start+100
        i = int(math.ceil(float(limit-start) / 100))

    print('metadata collection complete')
    print('creating master json file')
    logfile = open(output_file_log,'a')
    try:
        with open(output_file, 'a') as outfile:
            for go in range(i):
                print('currently getting {} - {}'.format(start, end))
                sleep(6)  # needed to prevent hitting API rate limit
                id_batch = ids[start:end]
                start += 100
                end += 100       
                backOffCounter = 1
                while True:
                    try:
                        tweets = []
                        get = False
                        subbatch = id_batch.copy()
                        j = 0
                        while (not get) and (j<=10):
                            if hydration_mode == "e":
                                tweets_ = api.lookup_statuses(subbatch,tweet_mode = "extended")
                            else:
                                tweets_ = api.lookup_statuses(subbatch)
                            tweets.extend(tweets_)
                            #print("iteration"+str(j)+"-"+str(len(tweets_)))
                            idgot = [x.id for x in tweets_]
                            subbatch = list(set(subbatch).difference(idgot))
                            if len(subbatch)>0:
                                get = False
                            else:
                                get = True
                            j += 1    
                        #print(len(tweets))
                        break
                    except tweepy.TweepyException as ex:
                        print('Caught the TweepError exception:\n %s' % ex)
                        sleep(30*backOffCounter)  # sleep a bit to see if connection Error is resolved before retrying
                        backOffCounter += 1  # increase backoff
                        continue
                print("Get %s" %(len(tweets)))
                for tweet in tweets:
                    json.dump(tweet._json, outfile)
                    outfile.write('\n')
                for logid in subbatch:
                    logfile.write(str(logid))
                    logfile.write('\n')
    except:
        print('exception: continuing to zip the file')

    outfile.close()
    logfile.close()    

    """
    print('creating ziped master json file')
    zf = zipfile.ZipFile('{}.zip'.format(output_file_noformat), mode='w')
    zf.write(output_file, compress_type=compression)
    zf.close()

    def is_retweet(entry):
        return 'retweeted_status' in entry.keys()

    def get_source(entry):
        if '<' in entry["source"]:
            return entry["source"].split('>')[1].split('<')[0]
        else:
            return entry["source"]
    
    
    print('creating minimized json master file')
    with open(output_file_short, 'w') as outfile:
        with open(output_file) as json_data:
            for tweet in json_data:
                data = json.loads(tweet) 
                if hydration_mode == "e":
                    text = data["full_text"]
                else:
                    text = data["text"]          
                t = {
                    "created_at": data["created_at"],
                    "text": text,
                    "in_reply_to_screen_name": data["in_reply_to_screen_name"],
                    "retweet_count": data["retweet_count"],
                    "favorite_count": data["favorite_count"],
                    "source": get_source(data),
                    "id_str": data["id_str"],
                    "is_retweet": is_retweet(data)
                }
                json.dump(t, outfile)
                outfile.write('\n')
        
    f = csv.writer(open('{}.csv'.format(output_file_noformat), 'w'))
    print('creating CSV version of minimized json master file') 
    fields = ["favorite_count", "source", "text", "in_reply_to_screen_name", "is_retweet", "created_at", "retweet_count", "id_str"]                
    f.writerow(fields)       
    with open(output_file_short) as master_file:
        for tweet in master_file:
            data = json.loads(tweet)            
            f.writerow([data["favorite_count"], data["source"], data["text"].encode('utf-8'), data["in_reply_to_screen_name"], data["is_retweet"], data["created_at"], data["retweet_count"], data["id_str"].encode('utf-8')])
    """

