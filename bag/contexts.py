from decimal import Decimal
from django.conf import settings


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0

    # settings.FREE_DELIVERY_TRESHOLD - reffers to the variable we created in settings.py
    if total < settings.FREE_DELIVERY_TRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_TRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_treshold': settings.FREE_DELIVERY_TRESHOLD,
        'grand_total': grand_total,
    }

    return context


# This is what's known as a context processor.
# And its purpose is to make this dictionary available to all templates across the entire application
# Much like you can use request.user in any template
# due to the presence of the built-in request context processor.
# In order to make this context processor available to the entire application
# we need to add it to the list of context processors in the templates variable in settings.py
# I'll add that here with "bag.contexts.bag_contents"
# This simple change means that anytime we need to access the bag contents
# in any template across the entire site they'll be available to us
# without having to return them from a whole bunch of different views across
# different apps.