import django_filters
from portfolio.models import Gig
from django import forms


class SingleChoiceSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs["onChange"] = "make_only_one_selected(event)"


class GigFilter(django_filters.FilterSet):
    # CHOICES = (
    #     ("ascending", "Lowest price"),
    #     ("desending", "Highest price"),
    # )
    # ordering = django_filters.ChoiceFilter(
    #     label="Ordering",
    #     choices=CHOICES,
    #     method="filter_by_order",
    #     widget=forms.RadioSelect(),
    #     empty_label="Newest",
    # )

    # def filter_by_order(self, queryset, name, value):
    #     expression = "price" if value == "ascending" else "-price"
    #     return queryset.order_by(expression)

    # price = django_filters.RangeFilter(label="Price range")
    category = django_filters.MultipleChoiceFilter(
        choices=Gig.CATEGORY_CHOICES,
        widget=SingleChoiceSelectMultiple(
            attrs={
                "class": "checkbox-input",
            }
        ),
    )

    class Meta:
        model = Gig
        fields = [
            # "price",
            "category",
        ]
