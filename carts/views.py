from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist


# Get the session_id to be used as cart_id
def _cart_id(request):  # _ private function
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# Populate the cart
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # Get the product
    product_variation = []
    # Populate the product attributes dynamically
    if request.method == 'POST':  # Product Variation
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                  variation_value__iexact=value)  # iexact accept text capitalized
                product_variation.append(variation)
            except:
                pass

    try:  # Cart counter
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    # Multiple items block
    is_cart_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)  # Get the Car item Object
        # existing_variations --> database
        # current variations --> product_variations
        # item_id --> database
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variations = item.variations.all()
            ex_var_list.append(list(existing_variations))
            id.append(item.id)

        if product_variation in ex_var_list:
            # Increase the cart quantity
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:  # Adding product variations by item
                    item.variations.clear()  # Clean the previously variations
                    item.variations.add(*product_variation)  # * Make sure to get all variations
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if len(product_variation) > 0:  # Adding product variations by item
            cart_item.variations.clear()  # Clean the previously variations
            cart_item.variations.add(*product_variation)  # * Make sure to get all variations
        cart_item.save()
    return redirect('cart')


# Remove item one by one
def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


# Remove items form the cart once for all
def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


# Cart structure
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart object
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)  # Activate list of items
        for cart_item in cart_items:  # Iterate cart items inside the cart
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100  # Tax and grand total maths
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass  # Ignoring

    # Content to be passed to html
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,

    }
    return render(request, 'store/cart.html', context)
