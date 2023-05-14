from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from django.urls import reverse
from django.conf import settings
from shortuuid.django_fields import ShortUUIDField
from places.fields import PlacesField


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):  # 2.
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):  # 3.
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# changes the name of uploaded image file
def upload_location(self, filename):
    file_base, extension = filename.split(".")
    image_name = f"profile_images/{self.id}-avatar.{extension}"
    return image_name


class User(AbstractUser):
    id = ShortUUIDField(
        length=9,
        alphabet="1234567890",
        primary_key=True,
    )
    username = None
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    is_freelancer = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    phone = PhoneNumberField(blank=True)
    avatar = models.ImageField(default="default.jpg", upload_to=upload_location)
    location = PlacesField()

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # resize saved image from ImageField
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 200 or img.width > 200:
            img.thumbnail((200, 200))
            img.save(self.avatar.path)

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})


class ProfileComment(models.Model):
    profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile_comments",
    )
    comment = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(
        choices=list(zip(range(1, 11), range(1, 11))), default=None, null=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="author_comments",
    )
    is_active = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-date"]
