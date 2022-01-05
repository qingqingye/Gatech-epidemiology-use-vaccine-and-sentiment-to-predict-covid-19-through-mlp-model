from extractclocation import getcarmenloc
from hydrator_sample import tweetshydrator
import numpy as np
import os

#reference
#https://github.com/thepanacealab/covid19_twitter/blob/master/COVID_19_dataset_Tutorial.ipynb

#Twitter API credentials
keyfile = r'api_keys_1.json'  

percent = 0.05
#input data directory
inputdatadir = r'raw data'
#output data directory
outputdatadir = r'hydrate files sample %s%%' %(int(percent*100))
if not os.path.exists(outputdatadir):
    os.makedirs(outputdatadir)
#hydrate tweets

start = '20201220'
end = '20210125'
allfilelist = []
"""
for root, dirs, files in os.walk(inputdatadir):
    if len(files)>0:  
        idfile = list(filter(lambda x: x.split('.')[0].endswith('clean-dataset'), files))[0]
        idfile = os.path.join(root,idfile)
        allfilelist.append(idfile)
"""
for f in os.listdir(inputdatadir):
    if f.split('.')[0].endswith('clean-dataset'):
        ts = f.split('_')[0].replace('-','')
        if (ts>=start) & (ts<=end):
            idfile = os.path.join(inputdatadir,f)
            allfilelist.append(idfile)

tken = int(keyfile.split('.')[0].split('_')[-1])
maxtok = 1
nlength = int(np.floor(len(allfilelist)/maxtok))
filelist = allfilelist[int(nlength*(tken-1)):int(min(len(allfilelist),(nlength*(tken-1)+nlength)))]

np.random.seed(5)

for idfile in filelist:
    print(idfile)
    #input file 
    rawfile = os.path.join(idfile)
    #output file
    hydrated_file = os.path.join(outputdatadir, '{}.json'.format( os.path.basename(idfile).split('.')[0] ))
    
    carmen_file = os.path.join(outputdatadir, '{}_carmen.json'.format( os.path.basename(idfile).split('.')[0] ))
    if not os.path.exists(carmen_file):
        #hydrate
        if not os.path.exists(hydrated_file):
            tweetshydrator(rawfile,hydrated_file,keyfile,percent=percent)
            #get carmen location
            getcarmenloc(hydrated_file,carmen_file)
        
        os.remove(hydrated_file)
    


    
    