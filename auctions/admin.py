from django.contrib import admin

from django.contrib import admin
from auctions.models import *

# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(AuctionBid)
admin.site.register(AuctionComment)
admin.site.register(AuctionWatchList)
