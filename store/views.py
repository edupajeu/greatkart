from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from carts.models import CartItem
from carts.views import _cart_id
from .models import Product
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:  # Product by category
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)  # Pagination for store page (builtin way to paginate)
        page = request.GET.get('page')  # Get the number page from the main url
        page_products = paginator.get_page(page)  # Store the products page
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')  # Get all products and order by id
        paginator = Paginator(products, 3)  # Define a limit of item to be shown in the pagination
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': page_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):  # Get all product details by slug
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:  # Check the keyword passed
        keyword = request.GET['keyword']  # Store the keyword
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) |
                                                                        Q(product_name__icontains=keyword))
            # Q is a query from Django that helps in conditions like in this case (OR)
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)
