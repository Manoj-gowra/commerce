from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing_page/<int:listing_id>",
         views.listing_page, name="listing_page"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("closing_bid/<int:listing_id>", views.closing_bid, name="closing_bid"),
    path("add_comments/<int:listing_id>",
         views.add_comments, name="add_comments"),
    path("Watchlist", views.Watchlist, name="Watchlist"),
    path("add_watchlist/<int:listing_id>",
         views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:listing_id>",
         views.remove_watchlist, name="remove_watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("mylistings", views.myListings, name="myListings")
]
