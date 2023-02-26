from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import FormView, DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required

from apps.users.forms import SignUpForm, ProfileAddressForm, ProfilePaymentForm
from apps.users.models import Profile, ProfileAddress, ProfilePayment, ShoppingCart, ShoppingCartLine
from apps.products.models import Product, ProductQuestion
from apps.orders.models import OrderLine
from apps.notifications.mixins import NotificationMixin
# Create your views here.
class SignUpView(FormView):
    """Users sign up view."""

    template_name = 'users/user/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)

class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = 'users/user/login.html'

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = 'users/user/logged_out.html'


class ProfileDetailView(LoginRequiredMixin, NotificationMixin, DetailView):
    model = Profile
    template_name = "users/user/profile.html"

    def get_object(self):
        return self.request.user.profile


class ProfileAddressListView(LoginRequiredMixin, NotificationMixin, ListView):
    model = ProfileAddress
    template_name = "users/address/list.html"
    context_object_name = 'addresses'

    def get_queryset(self):
        queryset = ProfileAddress.objects.filter(
            profile=self.request.user.profile
        )
        return queryset


class ProfileAddressCreateView(LoginRequiredMixin, NotificationMixin, CreateView):
    model = ProfileAddress
    template_name = "users/address/create.html"
    form_class = ProfileAddressForm
    success_url = reverse_lazy('users:address:list')

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('from_order',False):
            return reverse_lazy('orders:create')
        return super().get_success_url()

class ProfileAddressUpdateView(LoginRequiredMixin, NotificationMixin, UpdateView):
    model = ProfileAddress
    template_name = "users/address/edit.html"
    success_url = reverse_lazy('users:address:list')
    form_class = ProfileAddressForm

def delete_profile_address(request, pk):
    address = ProfileAddress.objects.get(pk=pk)
    address.delete()
    return redirect('users:address:list')

## PROFILE PAYMENT VIEWS
class ProfilePaymentListView(LoginRequiredMixin, NotificationMixin, ListView):
    model = ProfilePayment
    template_name = "users/payments/list.html"
    context_object_name = 'payment_cards'

    def get_queryset(self):
        queryset = self.model.objects.filter(
            profile=self.request.user.profile
        )
        return queryset

class ProfilePaymentCreateView(LoginRequiredMixin, NotificationMixin, CreateView):
    model = ProfilePayment
    template_name = "users/payments/create.html"
    form_class = ProfilePaymentForm
    success_url = reverse_lazy('users:paymentcard:list')

    def form_valid(self, form):
        card_provider = {
            '3': 'American Express',
            '4': 'Visa',
            '5': 'Mastercard'
        }
        form.instance.profile = self.request.user.profile
        form.instance.card_provider = card_provider.get(
            form.instance.card_number[0], 'Other'
        )
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('from_order',False):
            return reverse_lazy('orders:create')
        return super().get_success_url()

class ProfilePaymentUpdateView(LoginRequiredMixin, NotificationMixin, UpdateView):
    model = ProfilePayment
    template_name = "users/payments/edit.html"
    success_url = reverse_lazy('users:paymentcard:list')
    form_class = ProfilePaymentForm

def delete_profile_payment(request, pk):
    address = ProfilePayment.objects.get(pk=pk)
    address.delete()
    return redirect('users:paymentcard:list')

class PublishedProductsListView(LoginRequiredMixin, NotificationMixin, ListView):
    model = Product
    template_name = "users/published_products/list.html"
    context_object_name = 'published_products'

    def get_queryset(self):
        return Product.objects.filter(
            seller=self.request.user.profile
        )

class ShoppingCartView(LoginRequiredMixin, NotificationMixin, DetailView):
    model = ShoppingCart
    template_name = 'users/cart.html'
    context_object_name = 'cart'

    def get_object(self):
        return self.request.user.profile.shopping_cart

@login_required
def change_product_qty(request, pk):
    type = request.GET['type']
    line = get_object_or_404(ShoppingCartLine, pk=pk)
    if type == 'add':
        line.quantity += 1
    if type == 'subtract' and line.quantity > 0:
        line.quantity -= 1
    line.save()
    return redirect('users:cart:cart')

@login_required
def remove_item(request, pk):
    line = get_object_or_404(ShoppingCartLine, pk=pk)
    line.delete()
    return redirect('users:cart:cart')


class ProductQuestionListView(LoginRequiredMixin, NotificationMixin, ListView):
    model = ProductQuestion
    template_name = "products/questions/unanswered_questions.html"
    context_object_name = 'unanswered_questions'

    def get_queryset(self):
        return ProductQuestion.objects.filter(
            responder=self.request.user.profile,
            answer=''
        )

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['answered_questions'] = ProductQuestion.objects.filter(
            responder=self.request.user.profile,
        ).exclude(answer='')
        return context

@login_required
def product_not_received(request, pk):
    product_order = get_object_or_404(
        OrderLine,
        pk=pk,
        order__customer=request.user.profile
    )
    product_order.status = 'in_transit'
    product_order.save()
    return redirect('home')