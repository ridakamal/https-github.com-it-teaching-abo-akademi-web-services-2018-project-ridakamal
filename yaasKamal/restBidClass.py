from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from yaasKamal.models import Auction, Bids


class BidRestClass(APIView):


    def post(self, request):
        if request.user.is_authenticated:
            aId = request.POST['aId']
            priceForBid = request.POST['bid']
            priceForBid = float(priceForBid)
            auctionData = Auction.objects.get(id=aId)
            if request.user.is_authenticated:
                if request.user.username != auctionData.auctionOwner:

                    try:
                        totalBids = Bids.objects.filter(auctionKey=id)
                    except Exception:
                        totalBids = 0

                    if (auctionData.minPrice > priceForBid):
                        return Response({'message': 'Bid is lower than original price'})

                    else:

                        if (totalBids == 0 or len(totalBids) == 0):

                            biddingModel = Bids()
                            biddingModel.auctionKey = aId
                            biddingModel.auctionOwner = auctionData.auctionOwner
                            biddingModel.price = priceForBid
                            biddingModel.bidOwner = request.user.username
                            biddingModel.save()

                            return Response({'message': '/singleAuction/' + aId})

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

                                return Response({'message': 'Your Bid is too low or equal to the orignal price. Please make a greater Bid'})
                            elif (flag == 2):
                                return Response({'message': 'You have already made a bid. You will allowed to bid again, if someone makes greater bid than yours'})

                            else:

                                biddingModel = Bids()
                                biddingModel.auctionKey = aId
                                biddingModel.auctionOwner = auctionData.auctionOwner
                                biddingModel.price = priceForBid
                                biddingModel.bidOwner = request.user.username
                                biddingModel.save()
                                auctionData = Auction.objects.get(id=aId)
                                return Response({'message': 'Bid Made Successfully', 'data': auctionData})
                else:

                    return Response({'message': 'You can not Bid on your own Auction'})
            else:

                return Response({'message': '/login/'})
        else:

            return Response({'Request 404'})