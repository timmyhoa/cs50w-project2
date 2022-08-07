from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("create", views.create, name="create"),
    path("listing/<int:id>", views.showListing, name="showListing"),
    path("listing/<int:id>/closeListing", views.closeListing, name="closeListing"),
    path("listing/<int:id>/addBid", views.addBid, name="addBid"),
    path("listing/<int:id>/newComment", views.newComment, name="newComment"),
    path("listing/<int:id>/addWatchList", views.addWatchList, name="addWatchList"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchList", views.watchList, name="watchList"),
    
]
