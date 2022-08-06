from attr import field
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from .models import User, listing, bid, category
from .forms import *


def index(request):
    return render(request, "auctions/index.html", {
        'listings': listing.objects.all(),

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
    if request.method == "GET":
        currentListing = listing.objects.get(pk=id)
        return render(request, "auctions/showListing.html", {
            'listing': currentListing,
            'comments': comment.objects.filter(listing=currentListing),
            'createComment': createComment(),
        })
    
    newComment = createComment(request.POST)
    if newComment.is_valid():
        newComment = newComment.save(commit=False)
        newComment.user = request.user
        newComment.listing = listing.objects.get(pk=id)
        newComment.save()
        return HttpResponseRedirect(request.path)