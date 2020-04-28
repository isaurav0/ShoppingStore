from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    description = models.CharField(max_length=100, blank=False, default='')


class AuctionListing(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=1000, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=6,
                                       blank=False, default="0.00")
    listing_url = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.title


class AuctionBid(models.Model):
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,
                                blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=6, blank=False)

    class Meta:
        ordering = ('value',)

    def __str__(self):
        return self.auction.title


class AuctionComment(models.Model):
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,
                                blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.auction.title


class AuctionWatchList(models.Model):
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,
                                blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('auction',)

    def __str__(self):
        return self.auction.title
