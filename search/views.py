from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from users.models import Bibgroup, CustomUser
from .forms import DevkeyForm

import urllib.parse
import requests
import time
import csv

from search.models import Report, Journal, Author, SummaryReport, Summary
from search.tasks import add, adsquery, summaryquery

import logging


# Create your views here.


def index(request):
    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "search/index.html", context)
        #return render(request, "search/home.html", context)

    #otherwise, if they are logged in...
    username = request.user
    userid = username.id

    context = {
        "state": "loggedin",
        "first": username.first_name
        }

    return render(request, "search/index.html", context)
    #return render(request, "search/home.html", context)

#send user to login form
def login_form(request):
    context = {
            "state": "login",
            "error": ""
        }
    return render(request, "search/index.html", context)


#log user in
def login_view(request):
    username = request.POST["inputUsername"]
    password = request.POST["inputPassword"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        context = {
            "state": "login",
            "error": "Invalid credentials, try again."
            }
        return render(request, "search/index.html", context)


#log user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def account(request):
    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "search/index.html", context)
        #return render(request, "search/home.html", context)

    #otherwise, if they are logged in...
    username = request.user
    userid = username.id

    context = {
        "state": "loggedin",
        "error"  : "",
        "update" : ""
        }

    if request.method == 'POST':
        devk = request.POST["inputDevKey"]
        print(devk)

        username.devkey = devk
        username.save()

        context["update"] = "API Token Updated!"

    context["user"] = username

    devform = DevkeyForm(initial={"inputDevKey": username.devkey})
    pwform = PasswordChangeForm(request.user)

    context["devform"] = devform
    context["pwform"] = pwform

    return render(request, "search/account.html", context)

def help(request):

    context = {}

    return render(request, "search/help.html", context)

def about(request):

    context = {}

    return render(request, "search/about.html", context)

def search(request):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "search/index.html", context)

    #otherwise, if they are logged in...
    username = request.user
    userid = username.id

    bib = username.bibgroup
    bibgroups = Bibgroup.objects.all();

    context = {
        "err" : "",
        "bibgroups": bibgroups,
        "bib"   : bib
        }

    return render(request, "search/search.html", context)


def queued(request):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "search/index.html", context)

    #otherwise, if they are logged in...
    username = request.user
    userid = username.id

    context = {
        "err" : ""
        }

    namelist = request.POST["authorlist"]
    startdate = request.POST["startdate"]
    enddate = request.POST["enddate"]
    bibgroup = username.bibgroup #id
    bib = bibgroup.bibgroup #string
    daterange = startdate+" TO "+enddate

    devkey = username.devkey

    print (bibgroup.bibgroup)

    if namelist == "":
        error = "Please provide a name to search!"
        context ["err"] = error
        return render(request, "search/search.html", context)

    elif startdate == "" or enddate == "":
        error = "Please provide valid dates!"
        context["err"] = error
        return render(request, "search/search.html", context)

    else:

        authorlist = namelist.splitlines()
        makeset = Report.objects.create(username=username)
        makeset.namelist = namelist
        makeset.bibgroup_id = bibgroup.id

        makeset.save()

        reid = makeset.id

        #allsets = Report.objects.filter(username=username)

        print("Sending the query to ADS...")

        # send query to ADS via Celery...!
        adsquery.delay(namelist,daterange,bib,devkey,reid)
        
        makeset.save()
        
        context = {
            "namelist"  :  authorlist,
            "daterange" :  daterange,
            "bibgroup"  :  bib,
            #"allsets"   :  allsets,
            "curset"    :  reid,
            }

    return render(request, "search/queued.html", context)



def history(request):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "search/index.html", context)

    #otherwise, if they are logged in...
    username = request.user
    userid = username.id

    allsets = Report.objects.filter(username=username).order_by('-created')
    

    context = {
        "allsets"   :  allsets,
        }

    return render(request, "search/history.html", context)



def report(request, reid):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "search/index.html", context)

    #otherwise, if they are logged in...
    username = request.user
    userid = username.id

    resultset = Report.objects.get(id=reid)

    try:
    
        allauths = resultset.namelist.splitlines()
    
    except AttributeError:
        allauths = []

    #journals = Journal.objects.filter(resultset_id=reid,articlenum__gte=10).order_by('articlenum')

    journals = Journal.objects.filter(resultset_id=reid).order_by('articlenum')

    authors = Author.objects.filter(resultset_id=reid).order_by('rart')

    authnum1 = len(authors)

    jnum1 = (len(journals))#*60

    if jnum1*40 <= 300:
        jnum = 350
    else:
        jnum = jnum1*30

    if authnum1*40 <= 300:
        authnum = 350
    else:
        authnum = authnum1*40

    context = {
        "journals"  :  journals,
        "authors"   :  authors,
        "resultset" :  resultset,
        "allauths"  :  allauths,
        "authnum"   :  authnum,
        "jnum"      :  jnum
        }

    return render(request, "search/results.html", context)




def export_author(request):
    reid = request.POST["reid"]
    auths = Author.objects.filter(resultset_id=reid).order_by('aname')

    report = Report.objects.get(id=reid)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Authors_report'+reid+'_'+str(report.created)+'.csv"'

    writer = csv.writer(response)

    writer.writerow(["Author Name"]+["Total Articles"]+["Total Citations"]+["Refereed Articles"]+["Refereed Citations"]+["Non Refereed Articles"]+["Non Refereed Citations"])

    for x in auths:
        writer.writerow([x.aname]+[x.rart+x.nrart]+[x.rcite+x.nrcite]+[x.rart]+[x.rcite]+[x.nrart]+[x.nrcite])

    return response

def export_journal(request):
    reid = request.POST["reid"]
    jours = Journal.objects.filter(resultset_id=reid).order_by('-articlenum')

    report = Report.objects.get(id=reid)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Journals_report'+reid+'_'+str(report.created)+'.csv"'

    writer = csv.writer(response)

    writer.writerow(["Journal Name"]+["Total Articles"])

    for x in jours:
        writer.writerow([x.jname]+[x.articlenum])

    return response


def sumqueue(request):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "search/index.html", context)

    #otherwise, if they are logged in...
    username = request.user
    userid = username.id

    context = {
        "err" : ""
        }

    startdate = request.POST["startdate"]
    enddate = request.POST["enddate"]
    bibgroup = username.bibgroup #id
    bib = bibgroup.bibgroup #string
    daterange = startdate+" TO "+enddate

    devkey = username.devkey

    print (bibgroup.bibgroup)

    if startdate == "" or enddate == "":
        error = "Please provide valid dates!"
        context["err"] = error
        return render(request, "search/sumhistory.html", context)

    else:

        makeset = SummaryReport.objects.create(username=username)
        makeset.bibgroup_id = bibgroup.id
        makeset.save()

        reid = makeset.id

        #allsets = Report.objects.filter(username=username)

        print("Sending the query to ADS...")

        # send query to ADS via Celery...!
        summaryquery.delay(startdate,enddate,bib,devkey,reid)
        
        makeset.save()
        
        context = {
            "daterange" :  daterange,
            "bibgroup"  :  bib,
            "curset"    :  reid,
            }

    #return render(request, "search/sumhistory.html", context)
    return redirect(summaries)
    #return HttpResponseRedirect(reverse("index"))


def summaries(request):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "search/index.html", context)

    #otherwise, if they are logged in...
    username = request.user
    userid = username.id

    allsums = SummaryReport.objects.filter(username=username).order_by('-created')
    
    context = {
        "err" : "",
        "allsums"   :  allsums,
        "bib": username.bibgroup,
        }

    #response = redirect('/redirect-success/')
    return render(request, "search/sumhistory.html", context)




def summary(request, reid):

    #if they are NOT loggedin...
    if not request.user.is_authenticated:
        context = {
            "state": "home"
            }
        return render(request, "search/index.html", context)

    #otherwise, if they are logged in...
    username = request.user
    userid = username.id

    resultset = SummaryReport.objects.get(id=reid)

    summaries = Summary.objects.filter(resultset_id=reid).order_by('-year')

    context = {
        "resultset"  :  resultset,
        "summaries"   :  summaries,

        }

    return render(request, "search/summary.html", context)


def export_summary(request):
    reid = request.POST["reid"]
    summaries = Summary.objects.filter(resultset_id=reid).order_by('-year')

    report = SummaryReport.objects.get(id=reid)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Journals_report'+reid+'_'+str(report.created)+'.csv"'

    writer = csv.writer(response)

    writer.writerow(["Summary Report Created On"]+[report.created])
    writer.writerow(["Year"]+["Total Refereed Articles"]+["Total Citations"])

    for x in summaries:
        writer.writerow([x.year]+[x.refart]+[x.refcite])

    return response

"""

class Report(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    jnum = models.IntegerField(default=0)
    anum = models.IntegerField(default=0)
    daterange = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.username} {self.daterange}"


class Journal(models.Model):
    resultset = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True)
    jname = models.CharField(max_length=250, null=True, blank=True)
    articlenum = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.resultset} {self.jname} {self.articlenum}"




class Author(models.Model):
    resultset = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True)
    aname = models.CharField(max_length=250, null=True, blank=True)
    rart = models.IntegerField(default=0)
    nrart = models.IntegerField(default=0)
    rcite = models.IntegerField(default=0)
    nrcite = models.IntegerField(default=0)
    rfirst = models.IntegerField(default=0)
    nrfirst = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.resultset} {self.aname}"

"""