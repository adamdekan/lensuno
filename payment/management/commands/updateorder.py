from datetime import datetime, timedelta, timezone
from django.core.management.base import BaseCommand
from payment.models import Order


# https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/


class Command(BaseCommand):
    help = "Checks all orders and sets the status to completed for orders with date_time in the past"

    def handle(self, *args, **options):
        # get the current date and time
        now = datetime.now(timezone.utc)

        # loop through all orders
        for order in Order.objects.all():
            # calculate the number of days between the order date and the current date
            days_since_order = (now - order.date_time).days

            # check if the order is 7 or more days in the past
            if days_since_order >= 7:
                order.order_status = Order.OrderStatus.COMPLETED
                order.save()

        self.stdout.write(self.style.SUCCESS("Order statuses updated successfully!"))


# In the above code, we define a Command class that inherits from BaseCommand. We define a handle method that is called when the management command is run.

# We get the current date and time using the datetime.now() method. We then loop through all Order objects using the Order.objects.all() method.

# For each Order object, we calculate the number of days between the order date and the current date using the days attribute of a timedelta object. If the number of days is greater than or equal to 7, we set the order_status to "completed" and save the object using the save() method.

# Finally, we print a success message to the console using the self.stdout.write method.

# To run this management command every day, you can use a task scheduler like cron on Linux or macOS, or the Task Scheduler on Windows. You can set up a recurring task that runs the management command at a specific time every day.
