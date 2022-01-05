import carmen
import json


def getcarmenloc(input_file,output_file):
    """
    Carmen
    https://github.com/mdredze/carmen-python
    """
    
    resolver = carmen.get_resolver()
    resolver.load_locations()
    
    outfile = open(output_file, 'w')
    #read json file
    with open(input_file, 'r',encoding='utf-8') as f:
        for line in f.readlines():
            tweet = json.loads(line)
            #get location
            location = resolver.resolve_tweet(tweet)
            if location is None:
                tweet['CarmenLoc'] = None
            else:
                locdict = {}
                try:
                    locdict['country'] = location[1].country
                except:
                    pass
                try:
                    locdict['state'] = location[1].state
                except:
                    pass
                try:
                    locdict['city'] = location[1].city
                except:
                    pass
                try:
                    locdict['known'] = location[1].known
                except:
                    pass
                try:
                    locdict['id'] = location[1].id
                except:
                    pass
                
                tweet['CarmenLoc'] = locdict
            #write file
            json.dump(tweet, outfile)
            outfile.write('\n')
    outfile.close()
