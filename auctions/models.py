from pydoc import describe
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField


class User(AbstractUser):
    pass

class category(models.Model):
    category = models.CharField(max_length=40)
    
    
    def __str__(self) -> str:
        return self.category

class listing(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField(blank=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name="same")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "listings", default='0')
    
    
    def __str__(self) -> str:
        return f'{self.user} : {self.title}'


class bid(models.Model):
    bid = models.DecimalField(decimal_places=2, max_digits=9)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE, related_name= "bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "bids", default='0')


    def __str__(self) -> str:
        return f"{self.listing} : {self.bid}"

class comment(models.Model):
    comment = models.CharField(max_length=500)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE, related_name= "comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "comment")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user}: {self.listing}: {self.time}'
        