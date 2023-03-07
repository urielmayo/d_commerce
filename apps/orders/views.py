from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.messages.views import SuccessMessageMixin

from apps.orders.models import Order, OrderLine
from apps.orders.forms import OrderForm
from apps.orders.mixins import CartNotEmptyMixin
from apps.notifications.models import Notification
from apps.notifications.mixins import NotificationMixin
# Create your views here.

class OrderCreateView(CartNotEmptyMixin, NotificationMixin, SuccessMessageMixin, CreateView):
    model = Order
    template_name = "orders/create.html"
    form_class = OrderForm
    success_url = reverse_lazy('orders:list')
    success_message = "Order created succesfully!"

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['cart'] = self.request.user.profile.shopping_cart
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['profile'] = self.request.user.profile
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        Notification.send_notification(
            sender=None,
            receiver=self.request.user.profile,
            title=f'Order creted: #{self.object.pk}',
            message='Congratulations! You have just  bought this item',
            url=reverse_lazy('orders:list')
        )
        return response

class OrderListView(LoginRequiredMixin, NotificationMixin, ListView):
    model = Order
    template_name = "orders/list.html"
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.profile).order_by('-create_date')

class OrderDetailView(LoginRequiredMixin, NotificationMixin, DetailView):
    model = Order
    template_name = "orders/detail.html"
    context_object_name = 'order'

class OrderLinesListView(LoginRequiredMixin, NotificationMixin, ListView):
    model = OrderLine
    template_name = "orders/sold_products.html"
    context_object_name = 'sold_products'

    def get_queryset(self):
        return OrderLine.objects.filter(
            product__seller=self.request.user.profile
        )

@login_required
def ship_product(request, pk):
    line = get_object_or_404(
        OrderLine,
        pk=pk,
        product__seller=request.user.profile
    )
    line.status = 'in_transit'
    line.save()
    Notification.send_notification(
        sender=request.user.profile,
        receiver=line.order.customer,
        title='Your product has been shipped',
        message=f'Your {line.product.name} has been shipped. It will arrive in a few days',
        url=reverse_lazy('orders:list')
    )
    return redirect('orders:sales-list')

@login_required
def deliver_product(request, pk):
    line = get_object_or_404(
        OrderLine,
        pk=pk,
        product__seller=request.user.profile
    )
    line.status = 'delivered'
    line.save()
    Notification.send_notification(
        sender=request.user.profile,
        receiver=line.order.customer,
        title='Your product has been delivered',
        message=f'Your {line.product.name} has been delivered.\n'
        'If you enjoy it, please leave a review',
        url=reverse_lazy('orders:list')
    )
    return redirect('orders:sales-list')

@login_required
def cancel_order_line(request, pk):
    order_line = get_object_or_404(
        OrderLine,
        pk=pk,
        status='to_ship',
        order__customer=request.user.profile
    )
    order_line.status = 'cancelled'
    order_line.save()
    return redirect('orders:list')