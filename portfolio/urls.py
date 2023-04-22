from django.urls import path
from . import views

app_name = "portfolio"
urlpatterns = [
    path("start-portfolio/", views.start_portfolio, name="start"),
    path("step-one/", views.first_step, name="step-one"),
    path("step-two/", views.PortfolioCreateView.as_view(), name="create"),
    path("update/", views.portfolio_update_view, name="update"),
    # GIGS
    path("my-gigs/", views.gig_list_view, name="my-gigs"),
    path("gig/create/", views.GigCreateView.as_view(), name="gig-create"),
    path("gig/update/<slug:slug>/<int:pk>/", views.gig_update_view, name="gig-update"),
    path("gig/delete/<slug:slug>/<int:pk>/", views.gig_delete, name="gig-delete"),
    # PACKAGES
    path(
        "package/c/<str:package>/<int:gig_pk>/",
        views.create_package,
        name="package-create",
    ),
    path(
        "package/u/<str:package>/<int:gig_pk>/",
        views.update_package,
        name="package-update",
    ),
    path(
        "package/d/<str:package>/<int:gig_pk>/",
        views.delete_package,
        name="package-delete",
    ),
]
