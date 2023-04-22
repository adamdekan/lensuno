from django.contrib import admin
from .models import Comment

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_filter = ("rating",)
    list_display = (
        "author",
        "comment",
        "gig",
    )
    search_fields = ("author__email",)
    list_filter = ("is_flagged",)


admin.site.register(Comment, CommentAdmin)
