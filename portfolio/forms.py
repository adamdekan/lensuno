from .models import Package
from django import forms
from .models import Gig, Portfolio
from shootbe.widgets import CountableWidget
from django.core.validators import MinLengthValidator
from users.forms import FormTextField, FormFileField, FormNumberField


# https://github.com/RoboAndie/django-countable-field
class GigUpdateForm(forms.ModelForm):
    title = forms.CharField(widget=FormTextField())
    category = forms.ChoiceField(
        choices=Gig.CATEGORY_CHOICES,
        widget=forms.Select(
            attrs={"class": "add-listing__input js-example-basic-multiple"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget = CountableWidget(
            attrs={
                "data-count": "characters",
                "data-min-count": 30,
                "data-max-count": 1000,
                "class": "add-listing__textarea",
                "data-count-direction": "down",
            }
        )
        self.fields["deliverables"].widget = CountableWidget(
            attrs={
                "data-count": "characters",
                "data-min-count": 30,
                "data-max-count": 1000,
                "class": "add-listing__textarea",
                "data-count-direction": "down",
            }
        )
        self.fields["service"].widget = CountableWidget(
            attrs={
                "data-count": "characters",
                "data-min-count": 30,
                "data-max-count": 1000,
                "data-count-direction": "down",
                "class": "add-listing__textarea",
            }
        )
        self.fields["equipment"].widget = CountableWidget(
            attrs={
                "data-count": "characters",
                "data-min-count": 30,
                "data-max-count": 500,
                "data-count-direction": "down",
                "class": "add-listing__textarea",
            }
        )
        # self.fields["price"].label = "How much do you ask for this gig?"
        self.fields[
            "is_active"
        ].label = "Uncheck if you want to temporarily hide this gig"
        # self.fields["time"].label = "For how long are you hired?"

    class Meta:
        model = Gig
        fields = [
            "title",
            "category",
            "description",
            "deliverables",
            "service",
            "equipment",
            "is_active",
            "location",
        ]
        exclude = [
            "slug",
            "created_at",
            "wishlist_items",
        ]


class PortfolioUpdateForm(forms.ModelForm):
    slug = forms.SlugField(required=True, widget=FormTextField())
    website = forms.URLField(required=False, widget=FormTextField())
    social_ig = forms.CharField(required=False, widget=FormTextField())
    social_fb = forms.CharField(required=False, widget=FormTextField())
    social_yt = forms.CharField(required=False, widget=FormTextField())
    social_vm = forms.CharField(required=False, widget=FormTextField())
    photo = forms.ImageField(required=True, widget=FormFileField())
    about = forms.CharField(required=True)
    service = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].widget = CountableWidget(
            attrs={
                "data-count": "characters",
                "data-min-count": 30,
                "data-max-count": 1000,
                "data-count-direction": "down",
                "class": "add-listing__textarea",
            },
        )
        self.fields["about"].widget = CountableWidget(
            attrs={
                "data-count": "characters",
                "data-min-count": 30,
                "data-max-count": 140,
                "data-count-direction": "down",
                "class": "add-listing__textarea",
            }
        )
        self.fields["about"].label = "* Introduce yourself"
        self.fields["service"].label = "* Describe your service"
        self.fields["slug"].validators.append(
            MinLengthValidator(8, "Slug must be at least 8 characters."),
        )
        self.fields["website"].label = "URL to your website portfolio (optional)"
        self.fields["social_ig"].label = "URL to your Instagram portfolio (optional)"
        self.fields["social_fb"].label = "URL to your Facebook profile (optional)"
        self.fields["social_yt"].label = "URL to your YouTube channel (optional)"
        self.fields["social_vm"].label = "URL to your Vimeo channel (optional)"
        self.fields[
            "slug"
        ].label = "* Username of your portfolio between 8 - 15 characters"

    def clean_field(self):
        data = self.cleaned_data["social_ig"]
        if not data:
            data = "https://"

    class Meta:
        model = Portfolio
        fields = [
            "slug",
            "photo",
            "about",
            "service",
            "website",
            "social_ig",
            "social_fb",
            "social_yt",
            "social_vm",
        ]


class PackageForm(forms.ModelForm):
    price = forms.DecimalField(widget=FormNumberField())
    time = forms.IntegerField(widget=FormNumberField())

    class Meta:
        model = Package
        fields = ["price", "time", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget = CountableWidget(
            attrs={
                "data-count": "characters",
                "data-min-count": 30,
                "data-max-count": 255,
                "class": "add-listing__textarea",
                "data-count-direction": "down",
            }
        )

        self.fields["price"].label = "How much do you ask for this package?"
        self.fields["time"].label = "For how long are you hired?"
        self.fields["description"].label = "A short info about this package"
