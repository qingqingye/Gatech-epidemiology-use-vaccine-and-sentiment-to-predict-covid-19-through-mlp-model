import json
import tweepy
from tweepy import OAuthHandler
import os
"""
# Authenticate
CONSUMER_KEY = "yW9QON4EzjzmswRvAN53oWAzP" #@param {type:"string"}
CONSUMER_SECRET_KEY = "fupiN9yTbHVjXAg4M8PdaIACRM4NMBJHxsOKXhG5TvIFS6Rqvq" #@param {type:"string"}
ACCESS_TOKEN_KEY = "1240304078-8j7Qhtl5zcXyrF4g6JbY7ueWCEHU0COTZ5TukHd" #@param {type:"string"}
ACCESS_TOKEN_SECRET_KEY = "BJT08jP4VpYbK62lhYHVHHAk4t82XjQD3vr8x90fPWrVP" #@param {type:"string"}

#Creates a JSON Files with the API credentials
with open('api_keys_1.json', 'w') as outfile:
    json.dump({
    "consumer_key":CONSUMER_KEY,
    "consumer_secret":CONSUMER_SECRET_KEY,
    "access_token":ACCESS_TOKEN_KEY,
    "access_token_secret": ACCESS_TOKEN_SECRET_KEY
     }, outfile)

#The lines below are just to test if the twitter credentials are correct
# Authenticate
#auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)

#api = tweepy.API(auth, wait_on_rate_limit=True)

"""

# Authenticate
apikeys = {'key1':{'CONSUMER_KEY' : "yW9QON4EzjzmswRvAN53oWAzP" ,
                'CONSUMER_SECRET_KEY' :"fupiN9yTbHVjXAg4M8PdaIACRM4NMBJHxsOKXhG5TvIFS6Rqvq",
                'ACCESS_TOKEN_KEY' : "1240304078-8j7Qhtl5zcXyrF4g6JbY7ueWCEHU0COTZ5TukHd",
                'ACCESS_TOKEN_SECRET_KEY' : "BJT08jP4VpYbK62lhYHVHHAk4t82XjQD3vr8x90fPWrVP"},
         'key2':{'CONSUMER_KEY' : "wqIVhsyewlkqrYEaY1tWL843s" ,
                'CONSUMER_SECRET_KEY' :"OJB6J9GfHnklcxxvkzTfVlB6IJ84PmydmK8sIMBCtcfiCZTGYt",
                'ACCESS_TOKEN_KEY' : "1240304078-MNC974qEkMbPGeD6PZGQhJa1xS7dhSeKM3cbzkV",
                'ACCESS_TOKEN_SECRET_KEY' : "cGDBcXQ7pEkKqFMGUHj80OVTFQtWLkK9ve31ENsoBBxBf"},
         'key3':{'CONSUMER_KEY' : "OHBesoDDzGih1qenNKSgKOrdo" ,
                'CONSUMER_SECRET_KEY' :"jUz20vfZnuUyH8PQJxi9uINPC9QdbuCJs0cjgVgHNhQcRB8Rsc",
                'ACCESS_TOKEN_KEY' : "1240304078-pepFqwRQZGCFwUaGl9Mc8I7pqoCID95auqJ6jGL",
                'ACCESS_TOKEN_SECRET_KEY' : "9BzB8nBMTqah4inoI8iZWaUgp4G3cttaPJJFehOWctzFa"},
         'key4':{'CONSUMER_KEY' : "jYVHdFtzuojRtxp0Nf2CSNiCn" ,
                'CONSUMER_SECRET_KEY' :"zvu0arSJ7OzCXftRo3761SV3zQ83Jwcf4SVNu3hoQefAOUvkj6",
                'ACCESS_TOKEN_KEY' : "1240304078-6it1ueBuJ6JT7vfFCrH3xn5zxNJzFeF0mFDNgol",
                'ACCESS_TOKEN_SECRET_KEY' : "c7xJOxnYBsVqT2LCe54AlHOUhX39kx69EhTYPEbApd2Jz"},
         'key5':{'CONSUMER_KEY' : "BoNUFe2dmG4d7UevCufplnr7C" ,
                'CONSUMER_SECRET_KEY' :"PWM4NsiLRrpJ1geqOSXhWuq7dZ0FabFFTnDPzcbKBp9W0iSfRV",
                'ACCESS_TOKEN_KEY' : "1240304078-HXDDKwyov9Ws3aBmaYl7TOWcqzpDieb2heLY8nT",
                'ACCESS_TOKEN_SECRET_KEY' : "j7lAgqrogfcqOZOcIAb9y4AicoNjEAwJgC8Xv6eF92sLh"},
         'key6':{'CONSUMER_KEY' : "kxvZ2nPpFoaxWNnrtwygFrB7K" ,
                'CONSUMER_SECRET_KEY' :"0zxm9nadDxiBBkv9hS2ZmiTSBreLNFEQdAz5jW4IJBwitHRCqe",
                'ACCESS_TOKEN_KEY' : "1240304078-Szm0YPgTnAgawmYOv13MlVyMTfmBXymqjW83pb1",
                'ACCESS_TOKEN_SECRET_KEY' : "GCMOTFcDRxUlQehGHRkxl6dMowDWnXo4BcPbKAkm9hPZ8"},
         'key7':{'CONSUMER_KEY' : "alHFBa3Qhl3g51pLCsOntaRKY" ,
                'CONSUMER_SECRET_KEY' :"3oQfkspsm22hkK1KlxffgGoSZlUmSzXjlMBUe4jcvcN0KK2Y3H",
                'ACCESS_TOKEN_KEY' : "1240304078-gqnf1qgYNk6B2ssWU9FgylheEjw7aZih7VykuQE",
                'ACCESS_TOKEN_SECRET_KEY' : "JI7529O7o4rbrJXpzwgRDomgZvfUByUHY3Skw8F2qyyoi"},
         'key8':{'CONSUMER_KEY' : "9gsxNhmqHNct9MiU5gY5u5kyT" ,
                'CONSUMER_SECRET_KEY' :"rRIdH1df2vtr4SnNftnl3XbJ1iFhg1Yu0LXbvkvNLuhXHx4QnF",
                'ACCESS_TOKEN_KEY' : "1463922151623430152-goA2TQaphb4t0BXqeBIKmJvP0siYy4",
                'ACCESS_TOKEN_SECRET_KEY' : "kPhO8KLo2d6hQnKiyoX89wiTlMoLJMtWWKCLbPXByU2bF"},

         }


for key in apikeys.keys() :  
    print(key)      
    keyfile = 'api_keys_%s.json' %key[3:]
    if not os.path.exists(keyfile):
        #Creates a JSON Files with the API credentials
        with open(keyfile, 'w') as outfile:
            json.dump({
            "consumer_key":apikeys[key]['CONSUMER_KEY'],
            "consumer_secret":apikeys[key]['CONSUMER_SECRET_KEY'],
            "access_token":apikeys[key]['ACCESS_TOKEN_KEY'],
            "access_token_secret": apikeys[key]['ACCESS_TOKEN_SECRET_KEY']
             }, outfile)
            
        #test
        auth = tweepy.AppAuthHandler(apikeys[key]['CONSUMER_KEY'], apikeys[key]['CONSUMER_SECRET_KEY'])
    
        api = tweepy.API(auth, wait_on_rate_limit=True)
