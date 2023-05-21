from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, listings, Bid, Comments, Category, WatchList
from .forms import create_listingForm, place_bidForm, commentForm


def index(request):
    return render(
        request,
        "auctions/index.html",
        {"list_items": listings.objects.filter(sold=False)},
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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = create_listingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_bid = form.cleaned_data["start_bid"]
            image_url = form.cleaned_data["image_url"]
            category_id = Category.objects.get(id=request.POST["categories"])
            user = request.user
            if image_url == "":
                image_url = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
            listings.objects.create(
                user=user,
                title=title,
                description=description,
                starting_bid=start_bid,
                image_url=image_url,
                category=category_id,
            )
        return HttpResponseRedirect(reverse(index))
    else:
        if Category.objects.all().count()==0:
            categories = ["Electronics","Books","Kitchen","Clothing","Shoes","Furniture"]
            for item in categories:
                Category.objects.create(category=item)
        return render(
            request,
            "auctions/create_listing.html",
            {
                "listing_form": create_listingForm(),
                "categories": Category.objects.all(),
            },
        )


@login_required
def place_bid(request, listing_id):
    user = request.user
    listing = listings.objects.get(pk=listing_id)
    if request.method == "POST":
        form = place_bidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data["bid_amount"]
            if bid_amount > listing.starting_bid and bid_amount<1000:
                listing.starting_bid = float(bid_amount)
                listing.save()
                Bid.objects.create(user=user, list_bid=listing, bid_amount=bid_amount)
                return HttpResponseRedirect(reverse(index))
            else:
                return render(
                    request,
                    "auctions/listing_page.html",
                    {
                        "listing": listing,
                        "mssg": "Bid should more than the starting bid and less than 1000USD",
                        "BidForm": place_bidForm(),
                        "commentForm": commentForm(),
                        "Comments": Comments.objects.filter(listing=listing.id),
                    },
                )
    else:
        return render(
            request,
            "auctions/listing_page.html",
            {
                "listing": listing,
                "BidForm": place_bidForm(),
                "commentForm": commentForm(),
                "Comments": Comments.objects.filter(listing=listing.id),
            },
        )


@login_required(login_url="/login")
def listing_page(request, listing_id):
    listing = listings.objects.get(pk=listing_id)
    user = request.user
    code = False
    if listing.sold is True:
        try:
            winner = Bid.objects.get(
                bid_amount=listing.starting_bid, list_bid=listing.id
            ).user.username
        except:
            winner = "NO ONE"
        return render(
            request,
            "auctions/listing_page.html",
            {
                "listing": listing,
                "winner": winner,
                "commentForm": commentForm(),
                "Comments": Comments.objects.filter(listing=listing.id),
            },
        )
    if listing.user == user:
        code = True
        return render(
            request,
            "auctions/listing_page.html",
            {
                "listing": listing,
                "code": code,
                "commentForm": commentForm(),
                "Comments": Comments.objects.filter(listing=listing.id),
            },
        )
    else:
        watchin = WatchList.objects.filter(user=user, listing=listing)
        if watchin.exists():
            # print(WatchList.objects.get(user=user, listing=listing).watching)
            watch = WatchList.objects.get(user=user, listing=listing).watching
            return render(
                request,
                "auctions/listing_page.html",
                {
                    "listing": listing,
                    "code": code,
                    "BidForm": place_bidForm(),
                    "commentForm": commentForm(),
                    "watch": watch,
                    "Comments": Comments.objects.filter(listing=listing.id),
                },
            )
        else:
            watch = False
            return render(
                request,
                "auctions/listing_page.html",
                {
                    "listing": listing,
                    "code": code,
                    "BidForm": place_bidForm(),
                    "commentForm": commentForm(),
                    "watch": watch,
                    "Comments": Comments.objects.filter(listing=listing.id),
                },
            )


@login_required
def closing_bid(request, listing_id):
    listing = listings.objects.get(pk=listing_id)
    listing.sold = True
    listing.save()
    return listing_page(request, listing.id)


@login_required
def add_comments(request, listing_id):
    listing = listings.objects.get(pk=listing_id)
    user = request.user
    if request.method == "POST":
        form = commentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            Comments.objects.create(user=user, listing=listing, comment=comment)
        return redirect(listing_page, listing_id=listing.id)


@login_required
def Watchlist(request):
    user = request.user
    watchlist = WatchList.objects.filter(user=user, watching=True)
    if watchlist.exists():
        return render(request, "auctions/watchlist.html", {"watchlist": watchlist})
    else:
        return render(request, "auctions/watchlist.html", {"message": "is Empty "})


@login_required
def add_watchlist(request, listing_id):
    listing = listings.objects.get(pk=listing_id)
    user = request.user
    watchin = WatchList.objects.filter(user=user, listing=listing)
    if watchin.exists():
        watchin.delete()
        WatchList.objects.create(user=user, listing=listing, watching=True)
    else:
        WatchList.objects.create(user=user, listing=listing, watching=True)
    return redirect(listing_page, listing_id=listing.id)


@login_required
def remove_watchlist(request, listing_id):
    listing = listings.objects.get(pk=listing_id)
    user = request.user
    watchin = WatchList.objects.filter(user=user, listing=listing)
    watchin.delete()
    WatchList.objects.create(user=user, listing=listing, watching=False)
    return redirect(listing_page, listing_id=listing.id)


@login_required
def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})


@login_required
def category(request, category_id):
    listing = listings.objects.filter(category=category_id, sold=False)
    if listing.exists():
        return render(
            request,
            "auctions/list_by_category.html",
            {
                "listing": listing,
                "Category": Category.objects.get(pk=category_id).category,
            },
        )
    else:
        return render(
            request,
            "auctions/list_by_category.html",
            {
                "message": "No Items Found",
                "Category": Category.objects.get(pk=category_id).category,
            },
        )


@login_required
def myListings(request):
    user = request.user
    listing = listings.objects.filter(user=user)
    if listing.exists():
        return render(request, "auctions/myListings.html", {"listing": listing})
    else:
        return render(
            request, "auctions/myListings.html", {"message": "No items Found"}
        )
