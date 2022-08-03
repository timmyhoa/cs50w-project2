from pydoc import describe
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
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField()
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name="same")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "bids", default='0')
    def __str__(self) -> str:
        return f'{self.user} : {self.title}'


class bid(models.Model):
    bid = models.DecimalField(decimal_places=2, max_digits=9)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE, related_name= "bid")
    def __str__(self) -> str:
        return f"{self.listing} : {self.bid}"
        