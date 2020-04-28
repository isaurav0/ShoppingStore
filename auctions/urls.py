from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auctions/create", views.create_auction, name="create_auction"),
    url(r"auctions/search_by_category/(?P<category>\w+)/$",
        views.search_by_category, name="search_by_category"),
    url(r"auctions/place_bid/(?P<id>\w+)/$",
        views.place_bid, name="place_bid"),
    url(r"auctions/detail/(?P<id>\w+)/$",
        views.auction_detail, name="auction_detail"),
    path("auctions/watchlist", views.watchlist, name="watchlist"),
    url(r"auctions/add_to_watchlist/(?P<id>\w+)/$",
        views.add_to_watchlist, name="add_to_watchlist"),
    url(r"auctions/remove_from_watchlist/(?P<id>\w+)/$",
        views.remove_from_watchlist, name="remove_from_watchlist"),
    url(r"auctions/add_comment/(?P<id>\w+)/$",
        views.add_comment, name="add_comment"),
    url(r"auctions/close_auction/(?P<id>\w+)/$",
        views.close_auction, name="close_auction"),
    path("auctions/available_categories", views.available_categories,
         name="available_categories")
]
