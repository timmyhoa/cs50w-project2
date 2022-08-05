from attr import field
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from .models import User, listing, bid, category


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

            #Assignment expressions
            if (next := request.POST.get('next')) is not None:
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

class createListing(forms.ModelForm):
    class Meta:
        model = listing
        fields = ['title', 'description', 'image', 'category']
        widgets = {
            'image': forms.URLInput(attrs={
                'placeholder': "Image's url",
            })
        }

class createBid(forms.ModelForm):
    class Meta:
        model = bid
        fields = ['bid']
        labels = {'bid': ('Starting Price')}

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

