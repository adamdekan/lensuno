from django.urls import path
from . import views
from portfolio.views import gig_detail_view, PortfolioDetailView


app_name = "main"
urlpatterns = [
    # test page
    path("test/", views.test_page, name="test"),
    # path("search/<str:search>/", views.results, name="results"),
    # index page
    path("", views.Home.as_view(), name="index"),
    path("about/", views.about_us, name="about-us"),
    # path("404/", views.my_404_view, name="404"),
    path("copy-url/", views.copy_url, name="copy-url"),
    path("@<slug:slug>/", PortfolioDetailView.as_view(), name="portfolio-detail"),
    path("@<slug:slug>/<int:pk>/", gig_detail_view, name="gig-detail"),
    # path("switch-theme/", views.change_theme, name="change-theme"),
    # city search
    path("search/<str:search>/", views.search_city, name="search-city"),
    path("search/", views.search, name="search"),
    # path("search/", views.search_partial, name="search-partial"),
]
