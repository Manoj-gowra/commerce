from django.contrib import admin
from .models import User, Category, listings, Bid, Comments, WatchList
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(listings)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(WatchList)
