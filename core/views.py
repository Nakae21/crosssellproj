import json
import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Cart, CartItem, Order
from django.shortcuts import render
from .models import Product, Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm


def account_view(request):
    return render(request, 'core/account.html')

# View Cart Page
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    total = cart.get_total_price()
    return render(request, 'cart.html', {'cart': cart, 'total': total})

# Update Item Quantity
@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        item.quantity = max(1, quantity)
        item.save()
    return redirect('core:cart')

# Remove Item from Cart
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        item.delete()
    return redirect('core:cart')

# Paystack Checkout Initialization
@login_required
@csrf_exempt
def multi_checkout(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        total_amount = int(cart.get_total_price() * 100)  # Paystack uses kobo

        if total_amount == 0:
            return JsonResponse({'error': 'Your cart is empty.'}, status=400)

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        callback_url = request.build_absolute_uri('/verify/')
        payload = {
            "email": request.user.email,
            "amount": total_amount,
            "callback_url": callback_url
        }

        try:
            response = requests.post('https://api.paystack.co/transaction/initialize',
                                     headers=headers,
                                     json=payload)
            data = response.json()

            if data.get('status'):
                auth_url = data['data']['authorization_url']
                return JsonResponse({'auth_url': auth_url})
            else:
                return JsonResponse({'error': data.get('message', 'Payment init failed.')}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return HttpResponseBadRequest('Invalid request method')

# Paystack Callback/Verification
@login_required
def verify_payment(request):
    reference = request.GET.get('reference')

    if not reference:
        return HttpResponse("No payment reference provided.", status=400)

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    try:
        response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)
        data = response.json()

        if data['status'] and data['data']['status'] == 'success':
            # Save order record
            cart = Cart.objects.get(user=request.user)
            order = Order.objects.create(user=request.user, total=cart.get_total_price(), reference=reference)

            for item in cart.items.all():
                order.products.add(item.product)
            cart.items.all().delete()  # Empty cart after purchase

            return render(request, 'payment_success.html', {'order': order})
        else:
            return render(request, 'payment_failed.html', {'error': data.get('message', 'Payment failed.')})

    except Exception as e:
        return render(request, 'payment_failed.html', {'error': str(e)})


def product_list(request):
    products = Product.objects.all()
    cart = None
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'core/product_list.html', {
        'products': products,
        'cart': cart,
    })


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})
