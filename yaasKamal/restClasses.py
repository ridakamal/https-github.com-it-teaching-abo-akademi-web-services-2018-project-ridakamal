
from rest_framework.response import Response
from rest_framework.views import APIView

from yaasKamal.models import Auction

from yaasKamal import restSerializer



class AuctionRestClass(APIView):

    def post(self, request):


        userData = request.data

        title = userData['title']

        databaseData = Auction.objects.filter(title=title)
        if databaseData != {}:
            jsonObj = restSerializer.SerializeAuctionClass(databaseData, many=True)
            return Response(jsonObj.data)
        else:
            return Response({'Auction not registered in system'})

    def get(self, request):

        databaseData = Auction.objects.all()
        jsonObj = restSerializer.SerializeAuctionClass(databaseData, many=True)
        return Response(jsonObj.data)



