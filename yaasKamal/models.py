


from datetime import datetime, timedelta
from django.db import models

# Create your models here.

class Auction(models.Model):
    title           = models.CharField(max_length= 100);
    description     = models.TextField();
    creationDate      = models.DateTimeField(default = datetime.now)
    aLock     = models.TextField(default="")
    auctionOwner           = models.CharField(max_length=25)
    minPrice        = models.FloatField()
    deadline        = models.DateTimeField(default=datetime.now()+timedelta(days=3))
    adminBanned        = models.BooleanField(default= False)


    @classmethod
    def getById(cls, id):
        return cls.objects.get(id=id)

    @classmethod
    def exists(cls, id):
        return len(cls.objects.filter(id=id)) > 0

    def __unicode__(self):
        return self.title + ' / ' + self.auctionOwner + ' / '


class Bids(models.Model):
     auctionOwner = models.CharField(max_length= 100)
     auctionKey   = models.IntegerField()
     bidOwner     = models.CharField(max_length= 100)
     price = models.FloatField(null=False, blank=False)
     createDate = models.DateTimeField(default = datetime.now)


     def __unicode__(self):
         return self.auctionOwner + ' / '
