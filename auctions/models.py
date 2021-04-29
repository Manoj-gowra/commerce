from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):  # represent category of listings
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"


class listings(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="person_gives_lsiting")
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300, blank=True)
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2)
    image_url = models.URLField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="item_category")
    categories = models.ManyToManyField(
        Category, blank=True, related_name="select_category")
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} posted by {self.user}"


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="person_biding")
    list_bid = models.ForeignKey(
        listings, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=5, decimal_places=2)
    date_bid = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} = {self.bid_amount} on {self.list_bid.title} {self.date_bid}"


class Comments(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="person_commented")
    listing = models.ForeignKey(listings, on_delete=models.CASCADE)
    comment = models.TextField(max_length=300, blank=True)
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} : {self.comment}"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(listings, on_delete=models.CASCADE)
    watching = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} {self.listing.title} is {self.watching}"
