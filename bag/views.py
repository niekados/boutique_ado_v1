from django.shortcuts import render, redirect

# Create your views here.


def view_bag(request):
    """A view that renders the shopping bag content page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ add a quantity of the specified products to the shopping bag """
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
 
    return redirect(redirect_url)


# add_to_bag view
# The first thing we need to do is get the quantity from the form.
# So I can do that here with request.post.get quantity.
# And remember that we need to convert it to an integer since it'll come from the template as a string.
# We'll also want to get the redirect URL from the form so we know
# where to redirect once the process here is finished.
# Now for the missing piece of the puzzle. In modern versions of HTTP
# every request-response cycle between the server and the client
# in our case between the django view on the server-side and our form making the request on the client-side.
# Uses what's called a session, to allow information to be stored until the client and server are done communicating.
# This is especially handy in a situation like an e-commerce store
# Because it allows us to store the contents of the shopping bag
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