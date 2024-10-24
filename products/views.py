from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    # we set it to none, just to avoid errors when loading page without a search term
    query = None
    # same with category & sort & direction
    categories = None
    sort = None
    direction = None

    # The search phrase appears as GET
    if request.GET:
        if 'sort' in request.GET:

            # To clarify the reason for copying the sort parameter into a new variable called sortkey.
            # Is because now we've preserved the original field we want it to sort on name.
            # But we have the actual field we're going to sort on, lower_name in the sort key variable.
            # If we had just renamed sort itself to lower_name we would have lost the original field name.

            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            # In the sorting code block here I'll add a conditional to check if the sort key is equal to category.
            # And if it is I want to adjust it to tack on a double underscore and name.
            # Remember this double underscore syntax allows us to drill into a related model.
            # And that works for ordering also.
            # So by doing this we're effectively changing this line <products = products.order_by(sortkey)> to
            # products dot order by category double underscore name and of course if the
            # line above it adds a minus in front of it. it'll just be reversed.
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:

                # Moving on to the direction parameter. All we have to do here is check whether it's descending.
                # And if so we'll add a minus in front of the sort key using string formatting, which will reverse the order.

                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

                # in order to actually sort the products all we need to do is use the order by model method.
                products = products.order_by(sortkey)

        # If GET has 'category' in it
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)


        # If GET has a 'q' parameter in it
        if 'q' in request.GET:
            query = request.GET['q']
            # If the query is empty
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            # "i" in __icontains stands for "Case insensitive", '|' stands for "or"
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # The last thing I want to do is return the current sorting methodology to the template.
    # There are plenty of ways to do this but the easiest way is probably
    # just by using a string such as price_ascending name_descending and so on.
    # Since we have both the sort and the direction variables stored

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        # Note that the value of 'current_sorting' variable will be the string 'None_None'. If there is no sorting.
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """Add a product to the store"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """Edit Product in the store"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update Product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are edititng {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """Delete a product from the store"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
