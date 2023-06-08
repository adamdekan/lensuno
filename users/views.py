from django.shortcuts import render
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django_htmx.http import HttpResponseClientRefresh
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SettingsForm, FreelancerSignupForm
from django.contrib import messages
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from allauth.account.forms import (
    LoginForm,
    SignupForm,
)
from main.helpers import send_mail


def send_email_admin(subject, body):
    send_mail(
        subject,
        body,
        "admin@lensuno.com",
        ["lensunocom@gmail.com"],
        fail_silently=True,
    )


def signup_done(request):
    template = "main/sign-thanks.html"
    context = {}
    return TemplateResponse(request, template, context)


def signup_modal(request):
    context = {}
    template = "users/signup-form.html"
    if request.method == "POST":
        context["form_signup"] = form = SignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            email = form.cleaned_data.get("email")
            send_email_admin("New Signup", f"{email}")
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


def signup_freelancer(request):
    context = {}
    template = "users/onboarding.html"
    if request.method == "POST":
        context["form_signup"] = form = FreelancerSignupForm(request.POST)
        if form.is_valid():
            form.save(request)
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, email=email, password=password)
            auth_login(request, user)
            send_email_admin("New Onboarding Signup", f"{email}")
            return HttpResponseRedirect(reverse_lazy("portfolio:step-one"))
        else:
            return TemplateResponse(request, template, context)
    else:
        context["form_signup"] = FreelancerSignupForm()
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
