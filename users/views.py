from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import FormView, DetailView, ListView, CreateView, UpdateView

from users.forms import SignUpForm, ProfileAddressForm, ProfilePaymentForm
from users.models import Profile, ProfileAddress, ProfilePayment
# Create your views here.
class SignUpView(FormView):
    """Users sign up view."""

    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)

class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = 'users/login.html'

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = 'users/logged_out.html'


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "users/profile.html"

    def get_object(self):
        return self.request.user.profile


class ProfileAddressListView(LoginRequiredMixin, ListView):
    model = ProfileAddress
    template_name = "users/address/list.html"
    context_object_name = 'addresses'

    def get_queryset(self):
        queryset = ProfileAddress.objects.filter(
            profile=self.request.user.profile
        )
        return queryset


class ProfileAddressCreateView(LoginRequiredMixin, CreateView):
    model = ProfileAddress
    template_name = "users/address/create.html"
    form_class = ProfileAddressForm
    success_url = reverse_lazy('users:address-list')

    def get_form_kwargs(self):
        kwargs = super(ProfileAddressCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class ProfileAddressUpdateView(LoginRequiredMixin, UpdateView):
    model = ProfileAddress
    template_name = "users/address/edit.html"
    success_url = reverse_lazy('users:address-list')

    fields = [
        'main_street',
        'number',
        'secondary_street',
        'zip_code',
        'city',
        'country'
    ]

def delete_profile_address(request, pk):
    address = ProfileAddress.objects.get(pk=pk)
    address.delete()
    return redirect('users:address-list')

## PROFILE PAYMENT VIEWS
class ProfilePaymentListView(LoginRequiredMixin, ListView):
    model = ProfilePayment
    template_name = "users/payments/list.html"
    context_object_name = 'payment_cards'

    def get_queryset(self):
        queryset = self.model.objects.filter(
            profile=self.request.user.profile
        )
        return queryset

class ProfilePaymentCreateView(LoginRequiredMixin, CreateView):
    model = ProfilePayment
    template_name = "users/payments/create.html"
    form_class = ProfilePaymentForm
    success_url = reverse_lazy('users:paymentcard-list')

    def get_form_kwargs(self):
        kwargs = super(ProfilePaymentCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

class ProfilePaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = ProfilePayment
    template_name = "users/payments/edit.html"
    success_url = reverse_lazy('users:paymentcard-list')

    fields = [
        'card_number',
        'card_expiration_date'
    ]

def delete_profile_payment(request, pk):
    address = ProfilePayment.objects.get(pk=pk)
    address.delete()
    return redirect('users:paymentcard-list')