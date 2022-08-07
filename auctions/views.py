from attr import field
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse

from .models import User, listing, bid, category
from .forms import *


def index(request):
    return render(request, "auctions/index.html", {
        'listings': listing.objects.filter(active=True),

    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)

            #Assignment expressions
            if (next := request.POST.get('next')):
                return HttpResponseRedirect(next)
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


@login_required
def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            'formListing': createListing(),
            'formBid': createBid(),
        })
    
    #If request is POST:
    listingForm = createListing(request.POST)
    bidForm = createBid(request.POST)
    if listingForm.is_valid() and bidForm.is_valid():
        listingModel = listingForm.save(commit=False)
        listingModel.user = request.user
        listingModel.save()
        bidModel = bidForm.save(commit=False)
        bidModel.user = request.user
        bidModel.listing = listingModel
        bidModel.save()
        return HttpResponseRedirect(reverse('index'))
    return HttpResponseBadRequest()

def showListing(request, id):
    currentListing = listing.objects.get(pk=id)
    if not currentListing.active:
        show = False
    else:
        show = True
    return render(request, "auctions/showListing.html", {
        'listing': currentListing,
        'comments': comment.objects.filter(listing=currentListing)[::-1],
        'createComment': createComment(),
        'createBid': createBid(),
        'show': show,
    })


def closeListing(request, id):
    if request.method == "GET":
        return HttpResponseForbidden("Not allowed")
    currentListing = listing.objects.get(pk=id)
    currentListing.active = False
    currentListing.save()
    return HttpResponseRedirect(reverse('index'))

def addBid(request, id):
    currentListing = listing.objects.get(pk=id)
    if request.method == "GET":
        return HttpResponseForbidden("Not allowed")
    newBid = createBid(request.POST)
    if newBid.is_valid():
        newBid = newBid.save(commit=False)
    else:
        return HttpResponseBadRequest("Invalid Bid")
    if newBid.bid > currentListing.bid.last().bid:
        newBid.listing = currentListing
        newBid.user = request.user
        newBid.save()
        return HttpResponseRedirect(reverse('showListing', args=[currentListing.pk]))
    else:
        return HttpResponseBadRequest("Invalid Bid")

def newComment(request, id):
    currentListing = listing.objects.get(pk=id)
    newComment = createComment(request.POST)
    if newComment.is_valid():
        newComment = newComment.save(commit=False)
        newComment.user = request.user
        newComment.listing = currentListing
        newComment.save()
        return HttpResponseRedirect(reverse('showListing', args=[currentListing.pk]))
    else:
        return HttpResponseBadRequest("Please enter a valid comment")

def addWatchList(request, id):
    currentListing = listing.objects.get(pk=id)
    if request.POST['watchList'] == 'add':
        request.user.watchList.add(currentListing)
        request.user.save()
        return HttpResponseRedirect(reverse('showListing', args=[currentListing.id]))
    else:
        request.user.watchList.remove(currentListing)
        request.user.save()
        return HttpResponseRedirect(reverse('showListing', args=[currentListing.id]))


