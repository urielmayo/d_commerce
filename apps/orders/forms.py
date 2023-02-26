from django import forms

from apps.orders.models import Order, OrderLine
from apps.users.models import ProfileAddress, ProfilePayment
class OrderForm(forms.ModelForm):
    """Form definition for Order."""

    class Meta:
        """Meta definition for Orderform."""

        model = Order
        fields = (
            'customer_shipping_address',
            'customer_payment'
        )
        widgets = {
            'customer_shipping_address': forms.RadioSelect(),
            'customer_payment': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile')
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['customer_shipping_address'].queryset = self.profile.addresses.filter(
            type='shipping'
        )
        self.fields['customer_payment'].queryset = self.profile.payment_cards

    def save(self):
        data = self.cleaned_data
        profile = self.profile
        cart = self.profile.shopping_cart

        data.update({
            'customer': profile,
            'customer_billing_address': data['customer_shipping_address'],
            'status': 'paid',
            'subtotal': cart.total,
            'total': cart.total
        })
        order = Order(**data)
        order.save()

        for line in cart.get_lines_vals():
            OrderLine.objects.create(order=order, **line)

        for line in cart.shopping_cart_lines.all():
            line.product.stock_qty -= line.quantity
            line.product.save()
        cart.empty()

        return order

