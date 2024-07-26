from django.urls import path # type: ignore

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create/', views.create_auction_listing, name='create_auction_listing'),
    path('', views.active_listings, name='active_listings'),
    path('listing/<int:pk>/', views.auction_listing_detail, name='auction_listing_detail'),
    path('watchlist/', views.watchlist_view, name='watchlist'),
]
