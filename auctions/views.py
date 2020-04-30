from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, resolve
from .models import User, AuctionListing, AuctionBid,\
    AuctionWatchList, AuctionComment, Product, ProductCart


def search_by_category(request, category):
    return index(request, category=category)


@login_required
def index(request, watchlist=False, category=None):
    rows = list()

    # If category then get filtered results accordingly:
    if category:
        auctions = AuctionListing.objects.filter(
            closed=False, category=category)
    else:
        auctions = AuctionListing.objects.filter(
            closed=False)

    # Prepare data accordingly based on watchlist flag
    for auction in auctions:
        auction.watched = False

        # If the item is already watched, set watched=True
        if AuctionWatchList.objects.filter(
           auction=auction, user=request.user).exists():
            auction.watched = True
        # If watchlist is true and item in not watched, then ignore
        if watchlist and not auction.watched:
            continue

        auction.owner_item = False
        # If the item is created by logged in user, set owner_item flag True
        if auction.user == request.user:
            auction.owner_item = True

        # Add item to the rows
        rows.append(auction)

    # UI params
    params = {
        'rows': rows,
        'watchlist': watchlist,
    }

    return render(
        request,
        "products/main_product_choose.html",
        params
    )

@login_required
def create_auction(request):
    if request.method == "POST":

        # Read UI parameters
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        url = request.POST["url"]
        category = request.POST["category"]

        # Check if bid is missing
        if not starting_bid:
            error = 'Bid value missing'
            return render(request, "auctions/create_auction.html",
                          {'error': error})
        # Create listing
        response = AuctionListing.objects.create(
            title=title,
            description=description,
            user=request.user,
            starting_bid=starting_bid,
            listing_url=url,
            category=category

        )
        # #Return to home page
        message = "Successfully created a new post."
        messages.add_message(request, messages.SUCCESS, message)
        return redirect("index")

    else:
        return render(request, "auctions/create_auction.html")


@login_required
def auction_detail(request, id):
    # Check listing availability
    if not AuctionListing.objects.filter(id=id).exists():
        return(HttpResponse("Requested Item doesn't exist"))
    item = AuctionListing.objects.get(id=id)

    # Get highest bid for this listing
    item_bid = AuctionBid.objects.filter(auction=item).order_by("-value")
    highest_bid = item_bid[0].value if item_bid else item.starting_bid

    # Read comments for this listing
    comments = AuctionComment.objects.filter(
        auction=item).order_by("created_at")

    # Check if bid is won (applicable for closed listing)
    bid_won_flag = None
    if item.closed:
        bid_won_flag = bid_won(item_bid[0], request.user)

    # Prepare params to feed into the details template
    params = {
        'item': item,
        'highest_bid': highest_bid,
        'comments': comments,
        'bid_won': bid_won_flag,
    }
    return render(
        request,
        "auctions/auction_detail.html",
        params)


@login_required
def place_bid(request, id):
    # Check listing availability
    if not AuctionListing.objects.filter(id=id).exists():
        return HttpResponse("Requested Item doesn't exist")
    item = AuctionListing.objects.get(id=id)

    if request.method == "POST":
        # Read bid value from UI and convert to float
        bid_amount = request.POST["bid_amount"]
        try:
            bid_amount = float(bid_amount)
        except ValueError:
            error = "Invalid Bid Value."
            return index(request, error=error)

        # Read highest bid value on this item
        highest_bid = AuctionBid.objects.filter(
            auction=item).order_by("-value")
        highest_bid = highest_bid[0].value if highest_bid\
            else item.starting_bid

        # If supplied bid value is less than highest bid in the db
        if not bid_amount > highest_bid:
            error = "Bid value must be greater than {}".format(highest_bid)
            messages.add_message(request, messages.ERROR, error)
            return redirect("index")

        # Create bid
        response = AuctionBid.objects.create(
            auction=item,
            user=request.user,
            value=bid_amount
        )
        # Return to home page
        message = "Successfully placed bid."
        messages.add_message(request, messages.SUCCESS, message)
        return redirect("index")
    return render(request, "auctions/place_bid.html", {'item': item})


@login_required
def watchlist(request):
    # Return to home page with watchlist flag True
    return index(request, watchlist=True)


@login_required
def add_to_watchlist(request, id):
    # Check listing availability
    if not AuctionListing.objects.filter(id=id).exists():
        return HttpResponse("Requested Item doesn't exist")
    item = AuctionListing.objects.get(id=id)

    # Raise error if item is already in watchlist of loggedin user
    if AuctionWatchList.objects.filter(
       auction=item, user=request.user).exists():
        error = "Requested Item already in watchlist"
        messages.add_message(request, messages.ERROR, error)
        return redirect("index")

    # Add to watchlist
    response = AuctionWatchList.objects.create(
        auction=item,
        user=request.user,
    )

    # Return to home page
    message = "Successfully added to watchlist."
    messages.add_message(request, messages.SUCCESS, message)
    return redirect("index")


@login_required
def remove_from_watchlist(request, id):
    # Check listing availability
    if not AuctionListing.objects.filter(id=id).exists():
        return HttpResponse("Requested Item doesn't exist")
    item = AuctionListing.objects.get(id=id)

    # Raise error if item is not in watchlist
    if not AuctionWatchList.objects.filter(
       auction=item, user=request.user).exists():
        error = "Requested Item not in watchlist"
        messages.add_message(request, messages.ERROR, error)
        return redirect("index")
    # Remove from watchlist
    item = AuctionWatchList.objects.get(auction=item, user=request.user)
    item.delete()

    # Return to home page
    message = "Successfully removed from watchlist."
    messages.add_message(request, messages.SUCCESS, message)
    return redirect("index")


@login_required
def add_comment(request, id):
    # Check listing availability
    if not AuctionListing.objects.filter(id=id).exists():
        return HttpResponse("Requested Item doesn't exist")
    item = AuctionListing.objects.get(id=id)

    if request.method == "POST":
        # Read comment from UI
        comment = request.POST["comment"]

        # Add comment
        response = AuctionComment.objects.create(
            auction=item,
            user=request.user,
            comment=comment
        )
        # Return to home page
        message = "Successfully added a comment."
        messages.add_message(request, messages.SUCCESS, message)
        return redirect("index")
    return render(request, "auctions/add_comment.html", {'item': item})


@login_required
def close_auction(request, id):
    # Check login status
    if not request.user.is_authenticated:
        return render(request, "auctions/login.html", {
                "message": "User not logged in."
            })
    # Check listing availability
    if not AuctionListing.objects.filter(id=id, user=request.user).exists():
        return HttpResponse("Requested Item doesn't exist")
    item = AuctionListing.objects.get(id=id, user=request.user)

    # Update item and save
    item.closed = True
    item.save()

    # Return to home page
    message = "Successfully closed the listing."
    messages.add_message(request, messages.SUCCESS, message)
    return redirect("index")


@login_required
def available_categories(request):
    categories = AuctionListing.objects.order_by(
        'category').values('category').distinct()
    return render(request, "auctions/categories.html",
                  {'rows': categories})


@login_required
def bid_won(item_bid, session_user):
    """
    If session_user and the bid user is same, bid is won by this user
    """
    if not item_bid.user == session_user:
        return
    return True


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if not request.user.is_authenticated:
            return render(request, "auctions/login.html")
        return HttpResponseRedirect(reverse("index"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        description = request.POST["description"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, email, password, description=description)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def product_filter(request, category):
    _type = request.GET.get('type', 'THC')
    category = category.capitalize()
    print(category)
    print(_type)
    existing = Product.objects.filter(
        product_category=category,
        # product_type=_type
    )
    params = {
        'rows': existing
    }
    return render(request, "products/category.html", params)


def main_product_view(request):
    url_name = resolve(request.path).url_name
    params = {
        "url": url_name
    }
    return render(request, "products/choose.html", params)


def product_detail(request, product_id):
    try:
        product = Product.objects.get(
            pk=product_id,
        )

        try:
            existing_cart = ProductCart.objects.filter(product=product)
            if existing_cart:
                in_cart = True
            else:
                in_cart = False
        except Exception as e:
            in_cart = False
            print(e)

    except Product.DoesNotExist:
        return JsonResponse({"message": "Product Not Found"}, status=404)

    params = {
        'product': product,
        'in_cart': in_cart
    }
    return render(request, "products/product_detail.html", params)


def add_to_cart(request, product_id):

    if request.method == "POST":
        try:
            product = Product.objects.get(
                pk=product_id,
            )
        except Product.DoesNotExist:
            return JsonResponse({"message": "Product Not Found"}, status=404)

        existing_cart = ProductCart.objects.filter(product=product)
        if existing_cart:
            return JsonResponse({"message": "Product alreay in cart"}, status=400)
        response = ProductCart.objects.create(
            user=request.user,
            product=product,
        )
        # #Return to home page
        message = "Successfully added to cart."
        return JsonResponse({"message": message}, status=200)

    else:
        message = "GET request handler not found"
        return JsonResponse({"message": message}, status=404)


def remove_from_cart(request, product_id):

    if request.method == "POST":
        try:
            product = Product.objects.get(
                pk=product_id,
            )
        except Product.DoesNotExist:
            return JsonResponse({"message": "Product Not Found"}, status=404)
        try:
            # Delete cart entry
            existing = ProductCart.objects.get(
                user_id=request.user,
                product=product,
            )
            existing.delete()
            # #Return to home page
            message = "Successfully removed from cart."
            return JsonResponse({"message": message}, status=200)
        except ProductCart.DoesNotExist:
            message = "ERROR: Can't remove from cart"
            return JsonResponse({"message": message}, status=400)

    else:
        message = "GET request handler not found"
        return JsonResponse({"message": message}, status=404)