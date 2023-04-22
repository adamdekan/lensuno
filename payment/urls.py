from django.urls import path
from . import views

app_name = "payment"
urlpatterns = [
    path("order/<int:pk>/<str:package>/", views.create_order, name="order"),
    path("order/cancel/<int:pk>/", views.cancel_order, name="order-cancel"),
    path("order/confirm/<int:pk>/", views.confirm_order, name="order-confirm"),
    path("payment/", views.payment, name="payment"),
    path("my-orders/", views.my_orders, name="my-orders"),
    path("my-bookings/", views.my_bookings, name="my-bookings"),
]
