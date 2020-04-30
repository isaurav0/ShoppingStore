from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, resolve
from .models import User, Product, ProductCart,\
    ProductComment, ProductCommentReply


def search_by_category(request, category):
    return index(request, category=category)


@login_required
def index(request):
    return render(
        request,
        "products/main_product_choose.html"
    )


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
            return render(request, "products/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if not request.user.is_authenticated:
            return render(request, "products/login.html")
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
            return render(request, "products/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, email, password, description=description)
            user.save()
        except IntegrityError:
            return render(request, "products/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "products/register.html")


@login_required
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


@login_required
def main_product_view(request):
    url_name = resolve(request.path).url_name
    params = {
        "url": url_name
    }
    return render(request, "products/choose.html", params)


@login_required
def product_detail(request, product_id):
    try:
        product = Product.objects.get(
            pk=product_id,
        )

        comments = ProductComment.objects.get(
            pk=product_id
        )

        print(comments)

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


@login_required
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
            return JsonResponse({
                "message": "Product alreay in cart"}, status=400)
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


@login_required
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


@login_required
def add_comment(request, product_id):
    if request.method == "POST":

        product = Product.objects.filter(
            pk=product_id,
        )
        if not product:
            return JsonResponse({"message": "Product Not Found"}, status=404)

        # Read comment from UI
        comment = request.POST["comment_text"]

        # Add comment
        response = ProductComment.objects.create(
            product=product,
            user=request.user,
            comment=comment
        )

        # Return to home page
        message = "Successfully added a comment."
        messages.add_message(request, messages.SUCCESS, message)
        return JsonResponse({"message": "Product Not Found"}, status=200)


@login_required
def comment_reply(request, comment_id):
    comment = ProductComment.objects.filter(
        pk=comment_id,
    )
    if not comment:
        return JsonResponse({"message": "Comment Not Found"}, status=404)

    if request.method == "POST":
        # Read comment from UI
        reply = request.POST["reply"]

        # Add reply
        response = ProductCommentReply.objects.create(
            comment=comment,
            user=request.user,
            reply=reply
        )
        # Return to home page
        message = "Successfully replied on a comment."
        messages.add_message(request, messages.SUCCESS, message)
        return redirect("index")
    return render(request, "products/add_comment.html", {'item': item})
