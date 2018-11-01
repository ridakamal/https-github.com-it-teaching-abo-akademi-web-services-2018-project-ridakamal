from datetime import timedelta, datetime
from random import randint

from django.shortcuts import render
from urllib3.connectionpool import xrange

from .models import Auction
from .models import Bids
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.hashers import check_password
import json
from django.core.mail import send_mail
from django.core import mail
from django.utils import translation
import requests




# Create your views here.


def indexPage(request):
    if (request.user.is_authenticated):
        return HttpResponseRedirect('/viewAllAuctions/')
    else:
        return render(request, 'index.html')


def register(request):
    if (request.method == "GET"):
        return render(request, 'register.html')

    if (request.method == "POST"):

        email = request.POST['email']
        userName = request.POST['username']
        pwd = request.POST['password']

        user = User.objects.create_user(username=userName, password=pwd, email=email)
        user.save()
        return HttpResponseRedirect('/viewAllAuctions/')

    else:

        message = 'Error Loading page'
        return render(request, "error.html", {"errorMsg": message})


def login(request):
    if request.method == "GET":
        try:
            if request.GET['message']:
                message = request.GET['message']
                return render(request, 'login.html', {'message': message})
            else:
                return render(request, 'login.html')
        except Exception:
            return render(request, 'login.html')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/viewAllAuctions/')
        else:
            return render(request, 'error.html', {'errorMsg': 'Incorrect Username Or Password'})



def logOut(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def viewMyAuctions(request):
    sessionLogs = {}

    if ('vistedAuction' in request.session):
        sessionLogs['vistedCounter'] = request.session['vistedAuction']
    else:
        sessionLogs['vistedCounter'] = 0

    if ('createdAuction' in request.session):
        sessionLogs['createCounter'] = request.session['createdAuction']
    else:
        sessionLogs['createCounter'] = 0

    if ('deletedAunction' in request.session):
        sessionLogs['deleteCounter'] = request.session['deletedAunction']
    else:
        sessionLogs['deleteCounter'] = 0

    if ('editedAuction' in request.session):
        sessionLogs['editCounter'] = request.session['editedAuction']
    else:
        sessionLogs['editCounter'] = 0

    currencyCode = 3

    if request.user.is_authenticated and request.user.is_superuser:
        dbData = Auction.objects.filter(adminBanned=False, auctionOwner=request.user.username)
        rateOfExchange = liveCurrecyRate()
        if('moneySessionHandler' in request.session):
            moneySessionHandler = request.session['moneySessionHandler']
            moneySessionHandler = int(moneySessionHandler)
            if moneySessionHandler == 2:
                currencyCode = 2

                for value in dbData:
                    answer = value.minPrice / rateOfExchange
                    value.minPrice = (round(answer, 3))


            return render(request, 'viewMyAuction.html', {'data': dbData, 'sign': 2, 'currencyCode': currencyCode})

    if request.user.is_authenticated:
        dbData = Auction.objects.filter(auctionOwner=request.user.username)
        rateOfExchange = liveCurrecyRate()
        if ('moneySessionHandler' in request.session):
            moneySessionHandler = request.session['moneySessionHandler']
            moneySessionHandler = int(moneySessionHandler)
            if moneySessionHandler == 2:
                currencyCode = 2

                for value in dbData:
                    answer = value.minPrice / rateOfExchange
                    value.minPrice = (round(answer, 3))


        return render(request, 'viewMyAuction.html', {'data': dbData, 'sign': 1,'currencyCode': currencyCode})

    else:

        dbData = Auction.objects.all()
        rateOfExchange = liveCurrecyRate()
        if ('moneySessionHandler' in request.session):
            moneySessionHandler = request.session['moneySessionHandler']
            moneySessionHandler = int(moneySessionHandler)
            if moneySessionHandler == 2:
                currencyCode = 2

                for value in dbData:
                    answer = value.minPrice / rateOfExchange
                    value.minPrice = (round(answer, 3))

                for value in dbData:
                    value.minPrice = value.minPrice / rateOfExchange
        return render(request, 'viewMyAuction.html', {'data': dbData, 'sign': 0, 'currencyCode': currencyCode})


def viewAllAuctions(request):
    uId = 1
    currencyCode = 3
    rateOfExchange = liveCurrecyRate()
    dbData = Auction.objects.filter(adminBanned=False)
    if request.user.is_authenticated:

        if ('moneySessionHandler' in request.session):
            moneySessionHandler = request.session['moneySessionHandler']
            moneySessionHandler = int(moneySessionHandler)
            if moneySessionHandler == 2:
                currencyCode = 2

                for value in dbData:
                    answer = value.minPrice / rateOfExchange
                    value.minPrice = (round(answer, 3))


        return render(request, 'viewAllAuctions.html', {'data': dbData, 'sign': 1,'currencyCode': currencyCode})
    else:
        if ('moneySessionHandler' in request.session):
            moneySessionHandler = request.session['moneySessionHandler']
            moneySessionHandler = int(moneySessionHandler)
            if moneySessionHandler == 2:
                currencyCode = 2

                for value in dbData:
                    answer = value.minPrice / rateOfExchange
                    value.minPrice = (round(answer, 3))


        return render(request, 'viewAllAuctions.html', {'data': dbData, 'sign': 0,'currencyCode': currencyCode})

def singleAuctions(request, id):
    if (request.method == 'GET'):
        sessionLogs = {}
        currencyCode = 3

        if ('vistedBlog' in request.session):
            sessionLogs['vistCounter'] = request.session['vistedBlog']
        else:
            sessionLogs['vistCounter'] = 0

        auctionId = id
        dbData = Auction.objects.get(id=auctionId)
        bidData = Bids.objects.filter(auctionKey=auctionId)
        user = User()
        check_superUser = user.is_superuser

        if request.user.is_authenticated and request.user.is_superuser:
            rateOfExchange = liveCurrecyRate()
            if ('moneySessionHandler' in request.session):
                moneySessionHandler = request.session['moneySessionHandler']
                moneySessionHandler = int(moneySessionHandler)
                if moneySessionHandler == 2:
                    currencyCode = 2

                    answer = dbData.minPrice / rateOfExchange
                    dbData.minPrice = (round(answer,3))

            return render(request, 'singleAuction.html', {'data': dbData, 'sign': 2, 'bidData': bidData,'currencyCode': currencyCode})
        if request.user.is_authenticated:

            rateOfExchange = liveCurrecyRate()
            if ('moneySessionHandler' in request.session):
                moneySessionHandler = request.session['moneySessionHandler']
                moneySessionHandler = int(moneySessionHandler)
                if moneySessionHandler == 2:
                    currencyCode = 2

                    answer = dbData.minPrice / rateOfExchange
                    dbData.minPrice = (round(answer, 3))

            return render(request, 'singleAuction.html', {'data': dbData, 'sign': 1, 'bidData': bidData, 'currencyCode': currencyCode})

        else:
            rateOfExchange = liveCurrecyRate()
            if ('moneySessionHandler' in request.session):
                moneySessionHandler = request.session['moneySessionHandler']
                moneySessionHandler = int(moneySessionHandler)
                if moneySessionHandler == 2:
                    currencyCode = 2

                    answer = dbData.minPrice / rateOfExchange
                    dbData.minPrice = (round(answer, 3))

            return render(request, 'singleAuction.html', {'data': dbData, 'sign': 0, 'bidData': bidData,'currencyCode': currencyCode})

def changeLanguage(request):
    if request.method == 'GET':
        return render(request, 'language.html', {'sign': 1})

    elif request.method == 'POST':
        codeForLanguage = request.POST['codeForLanguage']
        selectedLangauge = codeForLanguage
        translation.activate(selectedLangauge)
        request.session[translation.LANGUAGE_SESSION_KEY] = selectedLangauge
        return HttpResponseRedirect('/viewAllAuctions/')


def createAuction(request):
    if (request.method == 'GET'):
        if (request.user.is_authenticated):
            return render(request, 'makeAuction.html', {'sign': 2})

    if ('createdAuction' in request.session):

        counterValue = request.session['createdAuction']
        counterValue += 1
        request.session['createdAuction'] = counterValue

    else:

        counterValue = 1
        request.session['createdAuction'] = counterValue

    if (request.method == "POST"):

        if request.user.is_authenticated:
            newAuction = Auction()
            newAuction.title = request.POST['title']
            newAuction.description = request.POST['description']
            newAuction.aLock = 'open'
            newAuction.auctionOwner = request.user.username
            newAuction.minPrice = request.POST['minPrice']
            newAuction.deadline = request.POST['dates']
            newAuction.save()
            auctionDetail = Auction.objects.get(title=newAuction.title)

            links = 'http://localhost:8000/singleAuction/' + str(auctionDetail.id)
            messsgeBody = newAuction.title + ' has been created, for edit click the link: ' + links
            fromEmailAdd = 'rida@abo.fi'
            toEmailAdd = request.user.email
            emailSubject = 'New Auction has been Created'

            generateEmail(messsgeBody, fromEmailAdd, toEmailAdd, emailSubject)
            return HttpResponseRedirect('/viewAllAuctions/')

        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/viewAllAuctions/')


def createBiddings(request, id):
    if request.method == 'POST':

        aId = id
        priceForBid = request.POST['bid']
        priceForBid = float(priceForBid)
        auctionData = Auction.objects.get(id=aId)
        if request.user.is_authenticated:
            if (request.user.username != auctionData.auctionOwner):

                try:
                    totalBids = Bids.objects.filter(auctionKey=id)
                except Exception:
                    totalBids = 0

                if (auctionData.minPrice > priceForBid):
                   return render(request, 'error.html', {'errorMsg': 'Bid is lower than original price'})


                else:

                    if (totalBids == 0 or len(totalBids) == 0):

                        biddingModel = Bids()
                        biddingModel.auctionKey = aId
                        biddingModel.auctionOwner = auctionData.auctionOwner
                        biddingModel.price = priceForBid
                        biddingModel.bidOwner = request.user.username
                        biddingModel.save()

                        return HttpResponseRedirect('/singleAuction/' + aId)

                    else:

                        for bid in totalBids:

                            if (priceForBid > bid.price):
                                flag = 1
                            else:
                                flag = 0

                            if (request.user.username == bid.bidOwner):
                                flag = 2
                                break

                        if (flag == 0):
                            return render(request, 'error.html', {'errorMsg': 'Your Bid is too low or equal to the orignal price. Please make a greater Bid'})

                        elif (flag == 2):
                            return render(request, 'error.html', {'errorMsg': 'You have already made a bid. You will allowed to bid again, if someone makes greater bid than yours'} )


                        else:
                            biddingModel = Bids()
                            biddingModel.auctionKey = aId
                            biddingModel.auctionOwner = auctionData.auctionOwner
                            biddingModel.price = priceForBid
                            biddingModel.bidOwner = request.user.username
                            biddingModel.save()
                            return HttpResponseRedirect('/singleAuction/' + aId)
            else:

                return render(request, 'error.html', {'errorMsg': 'You can not Bid on your own Auction'})

        else:

            return HttpResponseRedirect('/login/')
    else:
        return render(request, 'error.html', {'errorMsg': 'Request 404'})


def changeAuctionDetails(request, id):
    if (request.method == 'GET'):
        iD = id
        dbCredentials = Auction.objects.get(id=iD)

        return render(request, 'changeAuction.html', {'data': dbCredentials, 'sign': 2})
    else:
        if (request.method == 'POST'):
            auctionId = id
            newDescription = request.POST['description']

            verifyUser = Auction.objects.get(id=auctionId)

            if request.user.is_authenticated:

                if verifyUser.auctionOwner == request.user.username:

                    dbData = Auction.objects.get(id=auctionId)
                    dbData.description = newDescription
                    dbData.save()
                    return HttpResponseRedirect('/singleAuction/' + auctionId)


                else:
                   return render(request, 'error.html', {'errorMsg': 'Un-Authorized Action'})

            else:
                return HttpResponseRedirect('/login/')

def searchAndBrowse(request):
    if (request.method == 'GET'):
        if (request.user.is_authenticated):
            return render(request, 'searchAndBrowse.html', {'sign': 1})
        else:
            return render(request, 'searchAndBrowse.html', {'sign': 0})
    else:
        if request.method == 'POST':
            titleOfAuction = request.POST['search']
            try:
                dbData = Auction.objects.get(title=titleOfAuction)
            except Exception:
                return render(request, 'error.html', {'errorMsg': 'No Auction Found'})

            return HttpResponseRedirect('/singleAuction/' + str(dbData.id))
        else:
            print('Bad Request Made')


def dbFixtures(request):

    titAuction= 'Database Fixture Auction:  '
    descAuction= 'Auction Details:  '
    minPrice= randint(50, 1000)
    dDate= makeAuctionDate()

    for loopIterater in xrange(1,50):
        if (request.method == "GET"):
            if request.user.is_authenticated:
                newAuction = Auction()
                newAuction.title= titAuction,loopIterater
                newAuction.description=descAuction , loopIterater
                newAuction.aLock='open'
                newAuction.auctionOwner=request.user.username
                newAuction.minPrice=minPrice
                newAuction.deadline = dDate
                newAuction.save()
            else:
                return HttpResponseRedirect('/login/')
    return HttpResponseRedirect('/viewAllAuctions/')




def editProfile(request):
    if (request.method == 'GET'):

        if (request.user.is_authenticated):
            dbData = User.objects.get(username=request.user.username)

            return render(request, 'editUserProfile.html', {'data': dbData})
        else:
            return HttpResponseRedirect('/login/')

    else:
        if (request.user.is_authenticated):
            dbData = User.objects.get(username=request.user.username)
            newEmail = request.POST['email']
            oldPwd = request.POST['oldPwd']
            newPwd = request.POST['newPwd']

            if (check_password(oldPwd, dbData.password)):
                dbData.set_password(newPwd)
                dbData.email = newEmail
                dbData.save()
            return HttpResponseRedirect('/viewAllAuctions/')

        else:
            return HttpResponseRedirect('/login/')


def generateEmail(msgBody, fromEmailAddress, toEmailAddress, subjectOfEmail):

    body = msgBody
    from_email = fromEmailAddress
    to_email = toEmailAddress
    send_mail(subjectOfEmail, body, from_email, [to_email, ], fail_silently=False)

def banAuction(request, id):
    aId = id
    if (request.user.is_authenticated and request.user.is_superuser):
        dbData = Auction.objects.get(id=aId)
        dbData.adminBanned = True
        dbData.save()
        return HttpResponseRedirect('/viewAllAuctions/')

    else:
       return render(request, 'error.html', {'errorMsg': 'Un-Authorized Operation'})





def makeAuctionDate():
    cDate = datetime.now()
    fDate = timedelta(days=5)
    dDate = cDate + fDate
    return dDate


# function for live currency rates

def liveCurrecyRate():

    payload = {'access_Key': '6c3c3f74eff1295e1b759091f99e3046', '&currencies': 'EUR,PKR='}
    responseofUrl = requests.get('http://apilayer.net/api/live?', params=payload)
    currencyObj = json.loads(responseofUrl.content)
    moneyObj = currencyObj['quotes']
    euro = moneyObj['USDEUR']
    currentRates = euro

    return currentRates

def changeCurreny(request):
    if request.method == 'GET':
        return render(request, 'currencyPage.html',  {'sign': 1})
    elif request.method == 'POST':
        codeForCurrency = request.POST['codeForCurrency']
        request.session['moneySessionHandler'] = codeForCurrency
        return HttpResponseRedirect('/viewAllAuctions/')



























