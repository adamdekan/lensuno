from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "date_time",
            "message",
        ]

        widgets = {
            "date_time": forms.TextInput(attrs={"type": "datetime-local"}),
            "message": forms.Textarea(attrs={"rows": 4}),
        }
