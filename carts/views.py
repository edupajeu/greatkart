from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product
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
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    # Multiple items block
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1  # cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    return redirect('cart')


# Remove item one by one
def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

# Remove items form the cart once for all
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
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
