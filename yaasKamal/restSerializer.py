from rest_framework import serializers
from .models import Auction
from .models import Bids


class SerializeAuctionClass(serializers.ModelSerializer):

    class Meta:

        model    = Auction
       # model    = Bids
        fields    = '__all__'
