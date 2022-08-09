from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Cart, CartItem
from store.models import Product


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
        cart.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    #return HttpResponse(cart_item.quantity)
    return redirect('cart')


# Cart structure
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart object
        cart_item = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.qauntity)
            quantity += cart_item.quantity
    except ObejectNotExist:
        pass # Ignoring

    # Content to be passed to html
    context = {
        'total': total,
        'quantity': quantity,
        'cart_item': cart_items,
    }
    return render(request, 'store/cart.html')
