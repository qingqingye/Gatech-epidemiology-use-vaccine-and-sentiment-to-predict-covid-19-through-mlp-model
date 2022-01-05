import json
import pandas as pd
import os


# input data directory
input_data_dir = r'hydrate files sample 5%'

# output data directory
output_data_dir = r'tweets selected features 5%'

tweet_feature = ['created_at', 'full_text', 'entities', 'user', 'geo', "coordinates", 'place', 'is_quote_status',
                 'retweet_count', 'favorite_count', 'favorited', 'retweeted']

detailed_users = ['location', 'followers_count', 'friends_count', 'favourites_count']
detailed_entities = ['hashtags', 'symbols', 'user_mentions']
for filename in os.listdir(input_data_dir):
    print(filename)
    each_data = {}
    with open(os.path.join(input_data_dir, filename), 'r') as myfile:
        alldata = pd.read_json(myfile, lines = True)
        alldata_str = ''
        for i in range(len(alldata)):
            one_dir = alldata.loc[i]
            for j in range(len(tweet_feature)):
                if tweet_feature[j] == 'user':
                    temp_dir = {}
                    for k in range(len(detailed_users)):
                        temp_dir[detailed_users[k]] = one_dir['user'][detailed_users[k]]
                    each_data['user'] = temp_dir
                elif tweet_feature[j] == 'entities':
                    temp_dir = {}
                    for k in range(len(detailed_entities)):
                        temp_dir[detailed_entities[k]] = one_dir['entities'][detailed_entities[k]]
                    each_data['entities'] = temp_dir
                else:
                    each_data[tweet_feature[j]] = str(one_dir[tweet_feature[j]])
            each_data_json = json.dumps(each_data)
            alldata_str = alldata_str + each_data_json + '\n'
    
        #output the file        
        with open(os.path.join(output_data_dir,filename), "w") as outfile:
            outfile.write(alldata_str)

