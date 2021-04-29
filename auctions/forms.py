from django import forms
from .models import listings, Category, Bid, Comments


class create_listingForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=300)
    start_bid = forms.DecimalField(max_digits=5, decimal_places=2)
    image_url = forms.URLField()


class place_bidForm(forms.Form):
    bid_amount = forms.DecimalField(max_digits=5, decimal_places=2)


class commentForm(forms.Form):
    comment = forms.CharField(max_length=300)
