from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "gig",
        "buyer",
        "seller",
        # "created",
        # "delivery_date",
        "price",
    )
    list_filter = ("order_status",)
    search_fields = (
        "buyer__username",
        "seller__username",
    )


admin.site.register(Order, OrderAdmin)
