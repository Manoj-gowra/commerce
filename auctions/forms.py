from django import forms
from .models import listings, Category, Bid, Comments
from django.forms.widgets import Textarea


class create_listingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control col-md-9", "max_length": 50}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control col-md-9", "rows": 3, "max_length": 300}))
    start_bid = forms.DecimalField(widget=forms.NumberInput(
        attrs={"class": "form-control col-md-9", "max_digits": 5, "decimal_places": 2}))
    image_url = forms.URLField(label="Image URL (optional)",required=False, widget=forms.URLInput(attrs={"class": "form-control col-md-9"}))


class place_bidForm(forms.Form):
    bid_amount = forms.DecimalField(widget=forms.NumberInput(attrs={"class":"form-control","max_digits":5, "decimal_places": 2}))

class commentForm(forms.Form):
    comment = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "max_length": 300}))
