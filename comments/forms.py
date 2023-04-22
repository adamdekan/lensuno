from django import forms
from users.models import ProfileComment
from .models import Comment
from django.forms import widgets
from django_starfield import Stars  # https://pypi.org/project/django-starfield/


class CommentGigForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "contact-form__textarea",
                "placeholder": "Write a review...",
                "required": True,
            }
        )
    )
    # photo = forms.ImageField(
    #     required=False,
    #     widget=forms.FileInput(
    #         {
    #             "class": "contact-form__input-file",
    #         }
    #     ),
    # )

    rating = forms.IntegerField(
        required=False,
        widget=Stars,
    )  # https://pypi.org/project/django-starfield/

    class Meta:
        model = Comment
        fields = ["comment", "rating"]


class ReportCommentForm(forms.ModelForm):
    class Meta:
        model = ProfileComment
        fields = ["is_flagged"]


class CommentForm(CommentGigForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "contact-form__textarea",
                "placeholder": "Write a message for the user...",
                "required": True,
            }
        )
    )
    rating = forms.IntegerField(
        required=False,
        widget=Stars,
    )  # https://pypi.org/project/django-starfield/

    class Meta:
        model = ProfileComment
        fields = ["comment", "rating"]
