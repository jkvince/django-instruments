from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

# Create your views here.
def thanks(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)
    return render(request, 'thanks.html',{'customer_order':
customer_order})

class orderHistory(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            email = str(request.user.email)
            
            # Log email and check if orders are being filtered correctly
            print(f"User's email: {email}")
            
            # Fetch orders that belong to the logged-in user
            order_details = Order.objects.filter(emailAddress=email)
            
            # Log the fetched orders
            print(f"Fetched orders: {order_details}")
            
            # Rendering the correct template with order details
            return render(request, 'order/order_list.html', {'order_details': order_details})

class orderDetail(LoginRequiredMixin, View):
    def get(self, request, order_id):
        if request.user.is_authenticated:
            email = str(request.user.email)
            order = get_object_or_404(Order, id=order_id, emailAddress=email)
            order_items = OrderItem.objects.filter(order=order)
            return render(request, 'order/order_detail.html', {'order': order, 'order_items': order_items})
        else:
            return ('accounts:login') 