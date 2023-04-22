from django.urls import path, include
from . import views

app_name = "comments"

urlpatterns = [
    path(
        "report-gig-comment/<int:pk>/",
        views.report_gig_comment_htmx,
        name="report-gig-comment-htmx",
    ),
    path(
        "report-profile-comment/<int:pk>/",
        views.report_profile_comment_htmx,
        name="report-profile-comment-htmx",
    ),
]
