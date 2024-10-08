from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():  # bag.items is the bag from session
        # Check if item_data is integer. 
        # If it's an integer then we know the item data is just the quantity.
        # Otherwise we know it's a dictionary and we need to handle it differently.
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,

            })
        # So if item_data is dictionary (has sizes), we'll actually need to iterate through the inner dictionary of items_by_size
        # incrementing the product count and total accordingly.
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product': product,
                    'size': size,
                })


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