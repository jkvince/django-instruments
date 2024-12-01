from django.shortcuts import redirect, render, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.urls import reverse
from order.models import Order, OrderItem
from stripe import StripeError
from vouchers.models import Voucher
from vouchers.forms import VoucherApplyForm
from decimal import Decimal


def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        request.session.create()  # Create the session
        cart_id = request.session.session_key  # Retrieve the newly created session key
    return cart_id


def add_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
    
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
    if not created and cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    discount = 0
    voucher_id = 0
    new_total = 0
    voucher = None
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'Online Shop - New Order'
    voucher_apply_form = VoucherApplyForm()

    try:
        voucher_id = request.session.get('voucher_id')
        voucher = Voucher.objects.get(id=voucher_id)
        if voucher:
            discount = total * (voucher.discount / Decimal('100'))
            new_total = total - discount
            stripe_total = int(new_total * 100)
    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {'name': 'Order from Perfect Cushion Shop'},
                        'unit_amount': stripe_total,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                billing_address_collection='required',
                payment_intent_data={'description': description},
                success_url=request.build_absolute_uri(reverse('cart:new_order')) +
                             f"?session_id={{CHECKOUT_SESSION_ID}}&voucher_id={voucher_id}&cart_total={total}",
                cancel_url=request.build_absolute_uri(reverse('cart:cart_detail')),
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'counter': counter, 'error': str(e)})

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
        'voucher_apply_form': voucher_apply_form,
        'new_total': new_total,
        'voucher': voucher,
        'discount': discount
    })


def cart_remove(request, product_slug):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, slug=product_slug)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart:cart_detail')


def full_remove(request, product_slug):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, slug=product_slug)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')


def empty_cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        cart_items.delete()
        cart.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cart_detail')


def create_order(request):
    try:
        session_id = request.GET.get('session_id')
        cart_total = request.GET.get('cart_total')
        voucher_id = request.GET.get('voucher_id')

        if not session_id:
            raise ValueError("Session ID not found.")
        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except StripeError:
            return redirect("shop:all_products")

        customer_details = session.customer_details
        billing_address = customer_details.address
        billing_name = customer_details.name

        order_details = Order.objects.create(
            token=session.id,
            total=session.amount_total / 100,
            emailAddress=customer_details.email,
            billingName=billing_name,
            billingAddress1=billing_address.line1,
            billingCity=billing_address.city,
            billingPostcode=billing_address.postal_code,
            billingCountry=billing_address.country,
        )

        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)

        for item in cart_items:
            oi = OrderItem.objects.create(
                product=item.product.name,
                quantity=item.quantity,
                price=item.product.price,
                order=order_details
            )
            product = Product.objects.get(slug=item.product.slug)
            product.stock -= item.quantity
            product.save()
            oi.price *= oi.quantity
            oi.save()

        empty_cart(request)
        return redirect('order:thanks', order_details.id)

    except (ValueError, StripeError, ObjectDoesNotExist) as e:
        print(f"Error: {e}")
        return redirect("shop:all_products")
