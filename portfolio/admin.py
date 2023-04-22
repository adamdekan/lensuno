from django.contrib import admin
from .models import Portfolio, Gig


class PortfolioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "slug",
        "website",
    )
    list_filter = ("user", "is_featured")
    search_fields = ("user__email", "place")


class GigAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category")
    list_filter = ("category", "is_featured")
    search_fields = ("portfolio__user__email", "place")


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Gig, GigAdmin)
