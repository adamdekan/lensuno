from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import DemoGallery


class GalleryForm(forms.ModelForm):
    class Meta:
        model = DemoGallery
        fields = ["images"]

        # Remove label
        labels = {"images": ""}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields["images"].required = False

        self.fields["images"].max_number_of_images = 20

        from django.forms.widgets import Textarea  # noqa

        # self.fields["images"].widget = Textarea()
        # self.fields["images"].widget.attrs["readonly"] = True
        self.fields["images"].widget.template = "galleryfield/widget2.html"

        self.helper = FormHelper(self)
        self.helper.layout.append(
            Submit("Submit", "Submit", css_class="btn-default-red")
        )
