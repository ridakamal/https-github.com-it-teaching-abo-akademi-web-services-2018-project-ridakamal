from django.contrib import admin

from .models import Auction
from .models import Bids

# Register your models here.

admin.site.register(Auction)
admin.site.register(Bids)
