from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.


def view_bag(request):
    """A view that renders the shopping bag content page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ add a quantity of the specified products to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.name} to your shopping bag')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {product.name} to your shopping bag')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your shopping bag')

    request.session['bag'] = bag

    return redirect(redirect_url)


# add_to_bag view
# The first thing we need to do is get the quantity from the form. So I can do that here with request.post.get quantity.
# And remember that we need to convert it to an integer since it'll come from the template as a string.
# We'll also want to get the redirect URL from the form so we know where to redirect once the process here is finished.
# Now for the missing piece of the puzzle. In modern versions of HTTP every request-response cycle between the server and the client
# in our case between the django view on the server-side and our form making the request on the client-side.
# Uses what's called a session, to allow information to be stored until the client and server are done communicating.
# This is especially handy in a situation like an e-commerce store Because it allows us to store the contents of the shopping bag
# in the HTTP session while the user browses the site and adds items to be purchased. By storing the shopping bag in the session.
# It will persist until the user closes their browser so that they can add something to the bag.
# Then browse to a different part of the site add something else and so on without losing the contents of their bag.
# To implement this concept I'm going to create a variable bag. Which accesses the requests session.
# Trying to get this variable if it already exists. And initializing it to an empty dictionary if it doesn't.
# In this way, we first check to see if there's a bag variable in the session. And if not we'll create one.
# Since I've now got a regular old Python object a dictionary.
# I can just stuff the product into it along with the quantity. To do that. Within the bag dictionary
# I'll just create a key of the items id and set it equal to the quantity. If the item is already in the bag in other words
# if there's already a key in the bag dictionary matching this product id. Then I'll increment its quantity accordingly.
# Now I just need to put the bag variable into the session. Which itself is just a python dictionary.
# So to review. We'll submit the form to this view including the product id and the quantity.
# Once in the view we'll get the bag variable if it exists in the session or create it if it doesn't.
# And finally we'll add the item to the bag or update the quantity if it already exists.
# And then overwrite the variable in the session with the updated version.
# All that's left now is to import redirect. And then redirect the user back to the redirect URL.


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your shopping bag')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your shopping bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

# adjust_bag view 
# which will be pretty similar to the add_to_bag view so I'll copy that to use as a base.
# It still takes the request and item id as parameters. And the entire top portion will be the same except we don't need the redirect URL since we'll always want
# to redirect back to the shopping bag page. Remember that this is coming from a form on the shopping bag page which will
# contain the new quantity the user wants in the bag. So the basic idea here is that if quantity is greater than zero we'll want to set the items quantity
# accordingly and otherwise we'll just remove the item. If there's a size. Of course we'll need to drill into the
# items by size dictionary, find that specific size and either set its quantity to the updated one or remove it if the quantity submitted is zero.
# If there's no size that logic is quite simple and we can remove the item entirely by using the pop function.
# These two operations are basically the same. They just need to be handled differently due to the more complex structure of the
# bag for items that have sizes. With that finished we just need to redirect back to the view bag URL. And I'll use the reverse function to do that.
# Importing it here at the top.


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your shopping bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your shopping bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)

# remove_from_bag view.
# To allow users to remove items directly without setting quantity to zero. I'll copy the adjust bag view since again this will be similar.
# And let's update the name and adjust a couple of things. We don't need the quantity in this view since the intended quantity is zero.
# Now if the user is removing a product with sizes. We want to remove only the specific size they requested.
# So if size is in request.post. We'll want to delete that size key in the items by size dictionary.
# Also if that's the only size they had in the bag. In other words, if the items by size dictionary is now empty which will evaluate to false.
# We might as well remove the entire item id so we don't end up with an empty items by size dictionary hanging around.
# We should also do this in the adjust bag view if the quantity is set to zero. So I'll copy this part up there and also fix this little typo on the pop function.
# If there is no size. Again removing the item is as simple as popping it out of the bag.
# Finally instead of returning a redirect. Because this view will be posted to from a JavaScript function.
# We want to return an actual 200 HTTP response. Implying that the item was successfully removed.
# Additionally, I'll wrap this entire block of code in a try block. And catch any exceptions that happen in order to return a 500 server error.
# In a future video we'll use this variable e to return the actual error message to the template in case anything goes wrong.
