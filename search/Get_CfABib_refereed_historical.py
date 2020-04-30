# coding: utf-8

import requests
import json
import csv
import time
import codecs
import cStringIO
from datetime import datetime
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

#NOTE: typical ADS API users have a limit of 50,000 total results and 200 results per page.
#As of Nov 12, 2014 this script is retrieving 44,451 results, so we're coming close to
#the limit of total results.

devkey = (open('dev_key.txt','r')).read() #txt file that only has your dev key

#authorlist = (open('si_authlist.txt','r')).read()

#a_list = authorlist.splitlines()

#auth_list = []
#for y in a_list:
#    print y
#    auth_list.append(y)
    
#print auth_list

bibgroup = "cfa"
#pubyear = 2016

pubrange = range(1974,2019)
print pubrange



class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

timestamp = datetime.now().strftime("%Y_%m%d_%H%M")


resultFile = open(bibgroup+"_bib_generated_on_"+timestamp+".csv",'wb')

wr = UnicodeWriter(resultFile,dialect='excel',quoting=csv.QUOTE_ALL)

#write header row
wr.writerow(['Year']+['Total Ref Articles']+['Total Citations'])


for y in pubrange:

    citation = 0

    url = 'https://api.adsabs.harvard.edu/v1/search/query/?q=bibgroup:'+bibgroup+'&fq=pubdate:'+str(y)+'&fq=property:refereed'
    print url #printing url for troubleshooting

    headers={'Authorization': 'Bearer '+devkey}
    content = requests.get(url, headers=headers)
    results=content.json()
    k = results['response']['docs'][0]

    print results['response']

    total = results['response']['numFound']
    print "Total Results: "+str(total)


    #how many times to loop
    loop = total/200
    print "Looping script "+str(loop+2)+" times."
    startnum = 0

    #looping a lot!
    for i in range (1,loop+2):
    #for i in range (1,3): #use this line instead of above for short testing
        print "Results Page "+str(i)
        url1 = url+'&start='+str(startnum)+'&rows=200&fl=citation_count'
        print url1

        headers = {'Authorization': 'Bearer '+devkey}
        content = requests.get(url1, headers=headers)
        results = content.json()

        docs = results['response']['docs']

        for x in docs:
            print x

            try:
                citation_count = x['citation_count']
            except KeyError:
                citation_count = 0   
        
            
            citation += citation_count
            print citation

        startnum += 200
        time.sleep(1)
                    
    
    row = [str(y)]+[str(total)]+[str(citation)]
    wr.writerow(row)       
    
        
resultFile.close()


print "Finished loops through all "+str(total)+" results!"