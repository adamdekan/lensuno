from django.db import models
from portfolio.models import Gig
from django.conf import settings
from django.urls import reverse
from shortuuid.django_fields import ShortUUIDField
from portfolio.models import Package


# Create your models here.
class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELED = "canceled", "Canceled"

    id = ShortUUIDField(
        length=9,
        alphabet="1234567890",
        primary_key=True,
    )
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buying"
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="selling"
    )
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_time = models.DateTimeField(blank=True)
    message = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(
        max_length=13, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )

    class Meta:
        ordering = ["date_time"]
        indexes = [
            models.Index(fields=["date_time"]),
        ]

    def __str__(self):
        return f"Order #{self.id} - {self.gig.title}"

    def get_absolute_url(self):
        return reverse("payment:order", kwargs={"pk": self.id})
