from django.contrib.auth import authenticate, login, logout # type: ignore
from django.db import IntegrityError # type: ignore
from django.http import HttpResponse, HttpResponseRedirect # type: ignore
from django.shortcuts import render # type: ignore
from django.urls import reverse # type: ignore

from .forms import AuctionListingForm, BidForm, CommentForm

from .models import AuctionListing, User, Watchlist


def index(request):
    return render(request, "auctions/index.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def create_auction_listing(request):
    if request.method == "POST":
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            auction_listing = form.save(commit=False)
            auction_listing.user = request.user
            auction_listing.save()
            return HttpResponseRedirect(reverse('auction_listing_detail', args=[auction_listing.pk]))
    else:
        form = AuctionListingForm()
    return render(request, 'auctions/create_auction_listing.html', {
        "form": form
        })

@login_required # type: ignore
def auction_listing_detail(request, pk):
    listing = get_object_or_404(AuctionListing, pk=pk) # type: ignore

    if request.method == 'POST':
        if 'watchlist' in request.POST:
            pass
        elif 'bid' in request.POST:
            pass
        elif 'close_auction' in request.POST:
            pass
        elif 'add_comment' in request.POST:
            pass

    bid_form = BidForm()
    comment_form = CommentForm()

    context = {
        'listing': listing,
        'bid_form': bid_form,
        'comment_form': comment_form,
    }
    return render(request, 'auctions/auction_listing_detail.html', context)

def active_listings(request):
    active_listings = AuctionListing.objects.filter(is_active=True)
    context = {
        "active_listing": active_listings
    }   
    return render(request, "auctions/active_listenings.html", context)

def watchlist_view(request):
    if not request.user.is_authenticated:
        return redirect('login') # type: ignore

    watchlist_items = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist.html', {
        "watchlist_items": watchlist_items
        })

        
