from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .services import CartManager, OutOfStockError, InvalidQuantityError

@login_required
def cart_detail(request):
    cart_manager = CartManager(request.user)
    return render(request, 'cart/detail.html', {
        'cart': cart_manager.cart,
        'total_price': cart_manager.calculate_total()
    })

@require_POST
@login_required
def cart_add(request, product_id):
    cart_manager = CartManager(request.user)
    try:
        quantity = int(request.POST.get('quantity', 1))
        cart_manager.add_to_cart(product_id, quantity)
        messages.success(request, "Product added to cart successfully!")
    except OutOfStockError as e:
        messages.error(request, str(e))
    except InvalidQuantityError as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, "An error occurred while adding to cart.")
    
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))

@require_POST
@login_required
def cart_remove(request, item_id):
    cart_manager = CartManager(request.user)
    cart_manager.remove_item(item_id)
    messages.success(request, "Item removed from cart.")
    return redirect('cart:cart_detail')

@require_POST
@login_required
def cart_update(request, item_id):
    cart_manager = CartManager(request.user)
    try:
        quantity = int(request.POST.get('quantity', 1))
        cart_manager.update_quantity(item_id, quantity)
        messages.success(request, "Cart updated.")
    except OutOfStockError as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, "An error occurred while updating cart.")
    
    return redirect('cart:cart_detail')
