from search.models import Report, Journal, Author, Summary, SummaryReport
from users.models import CustomUser
from cfabib.celery import app

import json
import time
import requests
import urllib.parse



@app.task
def add(x, y):
    print("adding?")
    return x + y


@app.task
def adsquery(namelist,daterange,bibgroup,devkey,reid):

        authorlist = namelist.splitlines()

        url = 'https://api.adsabs.harvard.edu/v1/search/query/?q='

        def getloop(query,daterange,devkey):
            q = 'author:%22'+ urllib.parse.quote(query) + '%22%20pubdate:%5B' + daterange + '%5D%20bibgroup:'+bibgroup
            headers = {'Authorization': 'Bearer '+devkey}
            content = requests.get(url + q, headers=headers)
            results = content.json()
            num = results['response']['numFound']
            return num


        #author query
        # args: author name, daterange, devkey
        def adsquery(query,daterange,devkey):
            #rows max value is 200
            rows = 200

            total = getloop(query,daterange,devkey)
            loop = total/rows  # loop per person

            startnum = 0

            total_art = 0

            ref_cite = 0
            nonref_cite = 0

            ref_art = 0
            nonref_art = 0

            firstauth_ref = 0
            firstauth_nonref = 0

            for i in range (0,int(loop+1)):

                q = 'author:%22'+urllib.parse.quote(query)+'%22%20pubdate:%5B'+daterange+'%5D%20bibgroup:'+bibgroup+'&fl=property,citation_count,pub&rows='+str(rows)+'&start='+str(startnum)

                #print (url + q)

                headers = {'Authorization': 'Bearer '+devkey}
                content = requests.get(url + q, headers=headers)
                results = content.json()
                docs = results['response']['docs']

                for x in docs:                  

                    try:
                        journal = str(x['pub'])
                        
                    except KeyError:
                        journal = ""

                    # if a journal entry exists, append it to the larger query list
                    journallist.append(journal)

                    # there must also be an article for this person
                    total_art += 1

                    try:
                        prop = x['property']
                        propclean = (' | ').join(prop)
                    except KeyError:
                        propclean = ''

                    try:
                        citations = int(x['citation_count'])
                    except KeyError:
                        citations = 0

                    if "not refereed" in propclean.lower():
                        nonref_cite += citations
                        nonref_art += 1
                        
                    elif "refereed" in propclean.lower():
                        ref_cite += citations
                        ref_art += 1

                    else:
                        print ("what?")
                        pass


                # first author query
                qf = 'first_author:%22'+urllib.parse.quote(query)+'%22%20pubdate:%5B'+daterange+'%5D%20bibgroup:'+bibgroup+'&fl=property&rows='+str(rows)+'&start='+str(startnum)
                
                contentf = requests.get(url + qf, headers=headers)
                resultsf = contentf.json()
                docsf = resultsf['response']['docs']

                for y in docsf:

                    try:
                        propf = y['property']
                        propcleanf = (' | ').join(propf)
                    except KeyError:
                        propcleanf = ''

                    if "not refereed" in propcleanf.lower():
                        firstauth_nonref += 1
                        
                    elif "refereed" in propcleanf.lower():
                        firstauth_ref += 1

                    else:
                        print ("what?")
                        pass

                startnum += rows

            return total_art, ref_art, nonref_art, ref_cite, nonref_cite, firstauth_ref, firstauth_nonref


        journallist = []
        alist = []

        authcount = 0

        for x in authorlist:
            authors = {}

            authors["name"] = x

            total_art, ref_art, nonref_art, ref_cite, nonref_cite, firstauth_ref, firstauth_nonref = adsquery(x,daterange,devkey)

            if total_art == 0:
                pass
            else:

                newauthor = Author.objects.create(resultset_id=reid,
                                                    aname=x,
                                                    rart=ref_art,
                                                    nrart=nonref_art,
                                                    rcite=ref_cite,
                                                    nrcite=nonref_cite,
                                                    rfirst=firstauth_ref,
                                                    nrfirst=firstauth_nonref)
                newauthor.save()

                authcount += 1


        # get the relevant result set
        resultset = Report.objects.get(id=reid)
        resultset.anum = authcount
        resultset.daterange = daterange
        uniquej = set(journallist)
        resultset.jnum = len(uniquej)
        resultset.save()


        for y in uniquej:
            jours = {}
            total_art = journallist.count(y)

            jours["journal"] = y
            jours["total_art"] = total_art

            newjournal = Journal.objects.create(resultset_id=reid,jname=y,articlenum=total_art)
            newjournal.save()



@app.task
def summaryquery(startyr, endyr,bibgroup,devkey,reid):

    pubrange = range(int(startyr),int(endyr)+1)

    for y in pubrange:

        citation = 0

        url = 'https://api.adsabs.harvard.edu/v1/search/query/?q=bibgroup:'+bibgroup+'&fq=pubdate:'+str(y)+'&fq=property:refereed'

        headers={'Authorization': 'Bearer '+devkey}
        content = requests.get(url, headers=headers)
        results=content.json()
        k = results['response']['docs'][0]

        total = results['response']['numFound']
        loop = total/200
        startnum = 0

        #looping a lot!
        for i in range (1,int(loop+2)):
        #for i in range (1,3): #use this line instead of above for short testing
            url1 = url+'&start='+str(startnum)+'&rows=200&fl=citation_count'
            
            headers = {'Authorization': 'Bearer '+devkey}
            content = requests.get(url1, headers=headers)
            results = content.json()

            docs = results['response']['docs']

            for x in docs:

                try:
                    citation_count = x['citation_count']
                except KeyError:
                    citation_count = 0   
                           
                citation += citation_count

            startnum += 200
            time.sleep(1)
                        
        newsummary = Summary.objects.create(resultset_id=reid,year=y,refart=total,refcite=citation)
        newsummary.save()

    daterange = str(startyr)+" TO "+str(endyr)
    resultset = SummaryReport.objects.get(id=reid)
    resultset.daterange = daterange
    resultset.save()



# # Create your tasks here
# from __future__ import absolute_import, unicode_literals

# from celery import shared_task
# #from demoapp.models import Widget


# @shared_task
# def add(x, y):
#     return x + y


# @shared_task
# def mul(x, y):
#     return x * y


# @shared_task
# def xsum(numbers):
#     return sum(numbers)


# # @shared_task
# # def count_widgets():
# #     return Widget.objects.count()


# # @shared_task
# # def rename_widget(widget_id, name):
# #     w = Widget.objects.get(id=widget_id)
# #     w.name = name
# #     w.save()