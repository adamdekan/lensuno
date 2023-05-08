from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django_htmx.http import HttpResponseClientRefresh
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, FormView, DetailView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView
from allauth.account.views import LoginView, SignupView
from allauth.account.signals import user_logged_in
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SettingsForm, UserSignInForm, UserSignupForm
from django.contrib import messages
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from allauth.account.forms import (
    LoginForm,
    SignupForm,
    ResetPasswordForm,
    ChangePasswordForm,
)


def signup_done(request):
    template = "users/signup-success.html"
    context = {}
    return TemplateResponse(request, template, context)


def signup_modal(request):
    context = {}
    template = "users/signup-form.html"
    if request.method == "POST":
        context["form_signup"] = form = SignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseClientRefresh()
        else:
            return TemplateResponse(request, template, context)
    else:
        context["form_signup"] = SignupForm()
    return TemplateResponse(request, template, context)


def signin_modal(request):
    context = {}
    template = "account/login.html"
    if request.method == "POST":
        context["form_signin"] = form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            form.save(request)
            return HttpResponseClientRefresh()
        else:
            return HttpResponseRedirect("/")
    else:
        context["form_signin"] = LoginForm()
    return TemplateResponse(request, template, context)


def sign(request):
    template = "users/sign-page.html"
    context = {}

    context["form_signin"] = form_login = LoginForm()
    context["form_signup"] = form_signup = SignupForm()

    if "submit-loggin" in request.POST:
        if form_login.is_valid():
            user = form_login.get_user()
            user_logged_in(request, user)
            form_login.save(request)
            return HttpResponseClientRefresh()
        else:
            return HttpResponseRedirect("/")
    elif "submit_signup" in request.POST:
        if form_signup.is_valid():
            form_signup.save(request)
            return HttpResponseClientRefresh()

    return TemplateResponse(request, template, context)


@login_required
def settings_view(request):
    user = request.user

    if request.method == "POST":
        form = SettingsForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(user.get_absolute_url())
        else:
            # print(form.errors)
            messages.error(request, print(form.errors))
            return render(request, "users/settings.html", {"form": form})

    form = SettingsForm(instance=user)
    return render(request, "users/settings.html", {"form": form})


class SettingsView(LoginRequiredMixin, FormView):
    form_class = SettingsForm
    template_name = "users/settings.html"

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.bio = form.cleaned_data["bio"]
        user.phone = form.cleaned_data["phone"]
        user.location = form.cleaned_data["location"]
        if form.cleaned_data["avatar"]:
            user.avatar = form.cleaned_data["avatar"]
        user.save()
        messages.success(self.request, "Settings changed.")
        return HttpResponseRedirect(user.get_absolute_url())

    def get_initial(self):
        user = self.request.user
        initial = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "bio": user.bio,
            "location": user.location,
            "phone": user.phone,
            "avatar": user.avatar,
        }
        return initial

    def post(self, request):
        form = SettingsForm(request.POST)
        if form.is_valid():
            print(1)
        else:
            print(form.errors)
        content = {"form": form}
        return render(request, "users/settings.html", content)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject"
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        "If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    success_url = reverse_lazy("main:index")


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "users/password_change.html"
