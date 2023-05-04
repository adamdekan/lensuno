from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from wishlist.models import WishlistItem
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from places.fields import PlacesField
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os

# Create your models here.
User = settings.AUTH_USER_MODEL


class PortfolioManager(models.Manager):
    pass


# upload location for GIG images
def upload_location_portfolio(self, filename):
    file_base, extension = filename.split(".")
    image_name = f"portfolios/{file_base}.{extension}"
    return image_name


class Portfolio(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="portfolio"
    )
    photo = models.FileField(default="default.jpg", upload_to=upload_location_portfolio)
    slug = models.SlugField(unique=True, blank=True, max_length=20)
    about = models.TextField(max_length=140, blank=True)
    service = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    website = models.URLField(blank=True)
    social_ig = models.URLField(blank=True)
    social_fb = models.URLField(blank=True)
    social_yt = models.URLField(blank=True)
    social_vm = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)

    objects = models.Manager()
    # query = PortfolioManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate the slug based on user's email and random characters
            short = self.user.email.split("@")[0]
            short = short.replace(".", "-")
            self.slug = f"{short}-{get_random_string(length=6)}"
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 1920 or img.width > 3072:
            aspect_ratio = img.width / img.height
            new_height = min(1920, img.height)
            new_width = min(3072, round(new_height * aspect_ratio))
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            # delete the previous image file
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        # save the resized image
        img.save(self.photo.path, quality=80, optimize=True, format="JPEG")

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("main:portfolio-detail", kwargs={"slug": self.slug})

    def get_id(self):
        return self.id

    class Meta:
        ordering = ["-created_at"]


# upload location for GIG images
def upload_location_gig(self, filename):
    file_base, extension = filename.split(".")
    image_name = f"gigs/{file_base}-gig.{extension}"
    return image_name


class GigManager(models.Manager):
    def active(self, user):
        return self.get_queryset().filter(
            is_active=True, gallery__isnull=False, portfolio__user=user
        )

    def is_owner(self, user):
        if user.pk == self.get_queryset().portfolio.user.pk:
            return True


class Gig(models.Model):
    CATEGORY_CHOICES = (
        ("AL", "Anniversary & Life Moments"),
        ("CP", "Commercial & Product"),
        ("EW", "Engagement & Wedding"),
        ("SP", "Studio & Portrait"),
        ("TV", "Travel & Vacation"),
        ("JD", "Journalism & Documentary"),
        ("EC", "Event & Conference"),
        ("DR", "Drone Shots"),
        ("PT", "Photo Retouch"),
        ("VE", "Video Editing"),
    )

    id = ShortUUIDField(
        length=9,
        alphabet="1234567890",
        primary_key=True,
    )
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="gigs"
    )
    title = models.CharField(max_length=35)
    wishlist_items = GenericRelation(WishlistItem)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    description = models.TextField(max_length=1000)
    deliverables = models.TextField(max_length=1000, blank=True)
    equipment = models.TextField(max_length=500, blank=True)
    service = models.TextField(max_length=1000, blank=True)
    photo = models.FileField(upload_to=upload_location_gig, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255)
    location = PlacesField()
    is_featured = models.BooleanField(default=False)

    objects = models.Manager()
    query = GigManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "main:gig-detail",
            kwargs={"slug": self.portfolio.slug, "pk": self.id},
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Gig, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-updated_at"]


@receiver(post_save, sender=Gig)
def create_package(sender, instance, created, **kwargs):
    if created:
        standard_package = Package(
            gig=instance,
            package_type="standard",
            price=0,
            time=0,
            description="",
        )
        standard_package.save()


class Package(models.Model):
    PACKAGE_TYPE_CHOICES = (
        ("standard", "Standard"),
        ("premium", "Premium"),
        ("master", "Master"),
    )
    gig = models.ForeignKey(Gig, on_delete=models.CASCADE, related_name="packages")
    package_type = models.CharField(
        max_length=10, choices=PACKAGE_TYPE_CHOICES, default="standard"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.IntegerField(blank=False)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        package_type_dict = dict(self.PACKAGE_TYPE_CHOICES)
        return f"{self.gig.title} - {package_type_dict[self.package_type]}"

    class Meta:
        unique_together = ("gig", "package_type")
