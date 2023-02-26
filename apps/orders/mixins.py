from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

class CartNotEmptyMixin(LoginRequiredMixin):

    url = reverse_lazy('users:cart:cart')

    def dispatch(self, request, *args, **kwargs):
        if request.user.profile.shopping_cart.is_empty():
            return redirect(self.url)
        return super(CartNotEmptyMixin, self).dispatch(request, *args, **kwargs)