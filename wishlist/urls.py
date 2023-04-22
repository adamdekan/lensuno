from django.urls import path
from . import views

app_name = "wishlist"
urlpatterns = [
    path("all/", views.index, name="index"),
    path("toggle/<int:product_id>-<str:style>/", views.toggle_item, name="toggle_item"),
]
