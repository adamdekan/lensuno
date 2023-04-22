from django.forms import TextInput, FileInput, ChoiceField, NumberInput, DecimalField
from django.forms.widgets import Textarea
from shootbe.widgets import CountableWidget
from django import forms
from country_list import countries_for_language
from django.contrib.auth import get_user_model
from allauth.account.forms import (
    LoginForm,
    SignupForm,
    ResetPasswordForm,
    ChangePasswordForm,
)
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

User = get_user_model()
country_choices = [(name, name) for code, name in countries_for_language("en")]


# for SignInView(LoginView)
# https://django-allauth.readthedocs.io/en/latest/forms.html#login-allauth-account-forms-loginform
class UserSignInForm(LoginForm):
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "sign-form__input-text",
                "type": "password",
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        )
    )
    remember = forms.CheckboxInput(attrs={"class": "sign-form__checkbox-style"})

    def login(self, *args, **kwargs):
        # Add your own processing here.
        # You must return the original result.
        return super(UserSignInForm, self).login(*args, **kwargs)


# for SignUpView(SignupView):
# https://django-allauth.readthedocs.io/en/latest/forms.html#signup-allauth-account-forms-signupform
class UserSignupForm(SignupForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "sign-form__input-text",
                "type": "first_name",
                "placeholder": "First name",
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "sign-form__input-text",
                "type": "first_name",
                "placeholder": "First name",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "sign-form__input-text",
                "type": "password",
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "sign-form__input-text",
                "type": "password",
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


# https://django-allauth.readthedocs.io/en/latest/forms.html#reset-password-allauth-account-forms-resetpasswordform
class MyCustomResetPasswordForm(ResetPasswordForm):
    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a string containing the email address supplied
        email_address = super(MyCustomResetPasswordForm, self).save(request)

        # Add your own processing here.

        # Ensure you return the original result
        return email_address


class MyCustomChangePasswordForm(ChangePasswordForm):
    def save(self):
        # Ensure you call the parent class's save.
        # .save() does not return anything
        super(MyCustomChangePasswordForm, self).save()

        # Add your own processing here.


class FormTextField(TextInput):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs["class"] = "add-listing__input"
        super().__init__(attrs=attrs)


class FormListField(ChoiceField):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs["class"] = "add-listing__input js-example-basic-multiple"
        super().__init__(attrs=attrs)


class FormFileField(FileInput):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        # attrs["class"] = "add-listing__input-file"
        # attrs["_"] = "on click transition opacity to 0 then remove me"
        super().__init__(attrs=attrs)


class FormBoxField(Textarea):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs["class"] = "add-listing__textarea"
        super().__init__(attrs=attrs)


class FormNumberField(NumberInput):
    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        attrs["class"] = "add-listing__input"
        super().__init__(attrs=attrs)


# for SettingsView(FormView):
class SettingsForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=FormTextField())
    last_name = forms.CharField(required=False, widget=FormTextField())
    bio = forms.CharField(required=False)
    avatar = forms.ImageField(required=False, widget=FormFileField())
    phone = PhoneNumberField(
        required=False,
        widget=PhoneNumberPrefixWidget(),
    )

    class Meta:
        model = User
        exclude = ["email", "password", "date_joined", "city", "country"]
        fields = [
            "first_name",
            "last_name",
            "bio",
            "avatar",
            "phone",
            "location",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["bio"].widget = CountableWidget(
            attrs={
                "data-count": "characters",
                "data-min-count": 30,
                "data-max-count": 250,
                "data-count-direction": "down",
                "class": "add-listing__textarea",
            }
        )
