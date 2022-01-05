import json
import pandas as pd
import os
import csv

# input data directory
input_data_dir = r'tweets selected features 5%'

featuredata=[]
for filename in os.listdir(input_data_dir):
    print(filename)
    date = filename[0:10]
    with open(os.path.join(input_data_dir, filename), 'r') as myfile:
        
        alldata = pd.read_json(myfile, lines = True)
        alldata_str = ''
        
        length = len(alldata)
        retweet_count = favorite_count = followers = friends = user_favorite = 0
        for i in range(len(alldata)):
            one_dir = alldata.loc[i]
            retweet_count += one_dir['retweet_count']
            favorite_count += one_dir['favorite_count']
            followers += one_dir['user']['followers_count']
            #print(one_dir['user']['friends_count'])
            friends += one_dir['user']['friends_count']
            user_favorite += one_dir['user']['favourites_count']
        #print(user_favorite)
        #print(followers)
        #print(friends)
    temp = pd.Series(index=['date','retweet', 'favorite', 'followers' , 'friends', 'user_favorite'],
                     data=[date,retweet_count/length, favorite_count/length, followers/length, friends/length, user_favorite/length] )    
    featuredata.append(temp)
featuredata = pd.concat(featuredata,axis=1).T
featuredata.to_csv('features-test 5%.csv', encoding='utf-8',index=False)
