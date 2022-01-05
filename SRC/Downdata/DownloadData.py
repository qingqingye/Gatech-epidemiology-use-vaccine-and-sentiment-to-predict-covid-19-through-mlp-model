from bs4 import BeautifulSoup
import requests
import os
import datetime


def crawler(url,downloaddir):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        attrs = link.attrs
        if 'id' in attrs.keys():
            if attrs['id'] == 'raw-url':
                newlink = attrs['href']
                filename = os.path.basename(newlink)
                file = os.path.join(downloaddir,filename)
                try:
                    with open(file, 'wb') as f:
                        r = requests.get(r'https://github.com'+newlink)
                        f.write(r.content)
                    print("Success")
                except:
                    print("Fail")
                    with open("log.txt", 'a') as f:
                        f.write(url)
                        f.write('\n')
                    continue

start = datetime.date(2021,9,30)
end = datetime.date(2021,10,31)
t = start
downloaddir = r'raw data'
while t<=end:
    ts = t.strftime('%Y-%m-%d')
    print(ts)
    url = r"https://github.com/thepanacealab/covid19_twitter/blob/master/dailies/%s/%s_clean-dataset.tsv.gz" %(ts,ts)
    t += datetime.timedelta(1)
    crawler(url,downloaddir)
