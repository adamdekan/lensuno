from datetime import datetime, timezone

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from portfolio.models import Gig, Package

from .forms import OrderForm
from .models import Order


def get_order_status(order):
    now = datetime.now(timezone.utc)
    days_since_order = (now - order.date_time).days
    if order.date_time is None:
        return "Error: date_time field is not set"
    if order.order_status == Order.OrderStatus.PENDING:
        return "Pending"
    if order.order_status == Order.OrderStatus.IN_PROGRESS:
        if order.date_time.date() == now.date():
            return "In Progress"
        elif days_since_order <= 7 and days_since_order > 0:
            return "Post Production"
        else:
            return "Upcoming"
    elif order.order_status == Order.OrderStatus.COMPLETED:
        return "Completed"
    elif order.order_status == Order.OrderStatus.CANCELED:
        return "Canceled"


@login_required
def create_order(request, pk, package):
    template = "payment/order.html"
    context = {}

    gig = get_object_or_404(Gig, id=pk)
    package = get_object_or_404(Package, gig__pk=pk, package_type=package)
    seller = gig.portfolio.user
    buyer = request.user
    price = package.price

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.gig = gig
            order.seller = seller
            order.buyer = buyer
            order.price = price
            order.package = package
            order.save()
            # send_calendar_email(request, seller.email, order.date_time)
            return redirect(reverse("payment:my-bookings"))
    else:
        form = OrderForm()

    context["package"] = package.package_type
    context["gig"] = gig
    context["form"] = form
    return TemplateResponse(request, template, context)


@csrf_exempt
@login_required
def cancel_order(request, pk):
    if request.htmx:
        order = Order.objects.get(pk=pk)
        order.order_status = Order.OrderStatus.CANCELED
        order.save()
        # ! send mail to users
        messages.success(request, "You have canceled this booking.")
        return redirect(request.META["HTTP_REFERER"])
    else:
        messages.error(request, "You can not cancel this booking.")
        return redirect(request.META["HTTP_REFERER"])


@csrf_exempt
@login_required
def confirm_order(request, pk):
    if request.htmx:
        order = Order.objects.get(pk=pk)
        order.order_status = Order.OrderStatus.IN_PROGRESS
        order.save()
        # ! send mail to users
        messages.success(request, "You have accepted this booking.")
        return redirect(request.META["HTTP_REFERER"])
    else:
        messages.error(request, "You can not accept this booking.")
        return redirect(request.META["HTTP_REFERER"])


@login_required
def payment(request):
    template = "payment/payment.html"
    context = {}
    return TemplateResponse(request, template, context)


def get_order_list(orders):
    # create a list of orders with their statuses included
    order_list = []
    for order in orders:
        order_status = get_order_status(order)
        print(order_status)
        order_list.append((order, order_status))
    return order_list


@login_required
def my_orders(request):
    template = "payment/my-orders.html"
    context = {}

    context["orders"] = get_order_list(request.user.selling.all())
    context["is_order"] = True

    return TemplateResponse(request, template, context)


@login_required
def my_bookings(request):
    template = "payment/my-orders.html"
    context = {}

    context["orders"] = get_order_list(request.user.buying.all())
    context["is_booking"] = True

    return TemplateResponse(request, template, context)


def send_calendar_email(request, recipient_email, event_date_time):
    # Convert the event date time to a timezone-aware datetime object
    # event_date_time = pytz.timezone("UTC").localize(event_date_time)
    # Retrieve the credentials from settings
    creds_dict = getattr(settings, "GOOGLE_OAUTH2_CREDENTIALS", {})
    creds = Credentials.from_authorized_user_info(info=creds_dict)

    # Create the Google Calendar event
    try:
        service = build("calendar", "v3", credentials=creds)
        event = {
            "summary": "Event Summary",
            "location": "Event Location",
            "description": "Event Description",
            "start": {
                "dateTime": event_date_time.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": (event_date_time + datetime.timedelta(hours=1)).isoformat(),
                "timeZone": "UTC",
            },
            "reminders": {
                "useDefault": True,
            },
        }
        created_event = (
            service.events().insert(calendarId="primary", body=event).execute()
        )

        # Generate the Google Calendar link for the event
        event_id = created_event["id"]
        link = f"https://calendar.google.com/calendar/event?eid={event_id}"

        # Render the email template
        subject = "Event Invitation"
        from_email = "your-email@example.com"
        to_email = recipient_email
        context = {
            "event_date_time": event_date_time,
            "link": link,
        }
        text_content = render_to_string("email/calendar.txt", context)
        html_content = render_to_string("email/calendar.html", context)

        # Send the email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except HttpError as error:
        print(f"An error occurred: {error}")
