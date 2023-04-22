from django.contrib import admin
from .models import User, ProfileComment


class CustomUserAdmin(admin.ModelAdmin):
    exclude = ("password",)
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "is_superuser")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_superuser",)
    readonly_fields = ("email",)


class ProfileCommentAdmin(admin.ModelAdmin):
    list_filter = ("rating",)
    list_display = (
        "author",
        "profile",
        "comment",
    )
    search_fields = (
        "author__email",
        "profile__email",
    )
    list_filter = ("is_flagged",)


admin.site.register(User)
admin.site.register(ProfileComment, ProfileCommentAdmin)
