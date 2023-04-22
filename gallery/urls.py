from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from galleryfield import image_views


app_name = "gallery"
urlpatterns = [
    path("create/<int:pk>", views.GalleryCreateView.as_view(), name="create"),
    path("update/<int:pk>", views.GalleryUpdateView.as_view(), name="update"),
    path(
        "gallery-detail/<int:pk>",
        views.GalleryDetailView.as_view(),
        name="gallery-detail",
    ),
]
