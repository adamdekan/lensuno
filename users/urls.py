from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from comments.views import profile_view

app_name = "users"
urlpatterns = [
    path("signup-hx/", views.signup_modal, name="signup-hx"),
    path("signin-hx/", views.signin_modal, name="signin-hx"),
    path("signup/check-email/", views.signup_done, name="signup-success"),
    path("sign/", views.sign, name="sign"),
    # path("", views.UsersList.as_view(), name="users"),
    path("<int:pk>/", profile_view, name="profile"),  # PROFILE website of every user
    path("settings/", views.settings_view, name="settings"),  # SETTINGS of user
    path(
        "signout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="signout",
    ),
    path("password-reset/", views.ResetPasswordView.as_view(), name="password-reset"),
    path(
        "password-change/", views.ChangePasswordView.as_view(), name="password-change"
    ),
]
