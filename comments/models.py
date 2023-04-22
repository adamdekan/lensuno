from django.db import models
from django.conf import settings
from django.urls import reverse
from portfolio.models import Gig
from django_resized import ResizedImageField


def upload_location_comment(self, filename):
    file_base, extension = filename.split(".")
    image_name = f"{self.id}-comment.{extension}"
    return image_name


# Create your models here.
class Comment(models.Model):
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name="gig_comment")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_comment",
    )
    comment = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(
        choices=list(zip(range(1, 11), range(1, 11))), default=None, null=True
    )
    photo = ResizedImageField(upload_to="comments")
    is_active = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse(
            "main:gig-detail",
            kwargs={"slug": self.gig.portfolio.slug, "id": self.gig.id},
        )

    class Meta:
        ordering = ["-date"]
