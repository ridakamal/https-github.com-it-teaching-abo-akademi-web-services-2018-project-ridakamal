"""YaaSProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from yaasKamal.restClasses import AuctionRestClass
from yaasKamal.restBidClass import BidRestClass
from yaasKamal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.indexPage),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^logOut/$', views.logOut),
    url(r'^viewMyAuctions/$', views.viewMyAuctions),
    url(r'^viewAllAuctions/$', views.viewAllAuctions),
    url(r'^createAuction/$', views.createAuction),
    url(r'^singleAuction/(?P<id>\d+)/$', views.singleAuctions),
    url(r'^changeAuctionDetails/(?P<id>\d+)$', views.changeAuctionDetails),
    url(r'^searchAndBrowse/$', views.searchAndBrowse),
    url(r'^editProfile/$', views.editProfile),
    url(r'^changeLanguage/$', views.changeLanguage),
    url(r'^banAuction/(?P<id>\d+)$', views.banAuction),
    url(r'^createDbFixtures/', views.dbFixtures),
    url(r'^createBidding/(?P<id>\d+)$', views.createBiddings),

    url(r'^restApiBrowse/', AuctionRestClass.as_view()),
    url(r'^restApiSearch/', AuctionRestClass.as_view()),
    url(r'^restApiBidding/', BidRestClass.as_view()),
     url(r'^convertCurrency/$', views.changeCurreny),

]
