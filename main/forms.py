from django import forms
from portfolio.models import Gig

search_choice = Gig.CATEGORY_CHOICES + (("", "All categories"),)


class SearchForm(forms.Form):
    category = forms.ChoiceField(
        choices=search_choice,
        widget=forms.Select(
            attrs={
                "class": "search-form__input search-form__input-location js-example-basic-multiple",
            }
        ),
    )
    search = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "search-form__input",
                "placeholder": "Where do you want to shoot?",
                "name": "search",
                "id": "search",
            }
        ),
        required=False,
    )


class IndexSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].widget.attrs["class"] = "discover__form-input"
