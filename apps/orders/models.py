from django.db import models

from apps.users.models import Profile, ProfileAddress, ProfilePayment
from apps.products.models import Product

# Create your models here.
class Order(models.Model):
    """Model definition for Order."""

    customer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    customer_billing_address = models.ForeignKey(
        ProfileAddress,
        related_name='billing_address',
        on_delete=models.DO_NOTHING,
        limit_choices_to={'type': 'billing'}
    )
    customer_shipping_address = models.ForeignKey(
        ProfileAddress,
        related_name='shipping_address',
        on_delete=models.DO_NOTHING,
        limit_choices_to={'type': 'shipping'}
    )
    customer_payment = models.ForeignKey(
        ProfilePayment,
        on_delete=models.CASCADE,
    )
    subtotal = models.FloatField()
    total_taxes = models.FloatField(blank=True, null=True)
    total = models.FloatField()
    status = models.CharField(
        choices=[
            ('draft', 'Draft'),
            ('paid', 'Paid'),
            ('on_ship', 'On Ship'),
            ('shipped', 'Shipped'),
            ('cancelled', 'Cancelled')
        ],
        default='draft',
        max_length=10
    )
    create_date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    class Meta:
        """Meta definition for Order."""

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        """Unicode representation of Order."""
        return f'Order #{self.pk}'

class OrderLine(models.Model):
    """Model definition for OrderLine."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_lines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    discount = models.FloatField(blank=True, null=True)
    unit_price = models.FloatField()
    line_total = models.FloatField()
    status = models.CharField(
        choices=[
            ('to_ship', 'To Ship'),
            ('in_transit', 'In Transit'),
            ('delivered', 'Delivered'),
        ],
        default='to_ship',
        max_length=30
    )

    class Meta:
        """Meta definition for OrderLine."""

        verbose_name = 'Order Line'
        verbose_name_plural = 'Order Lines'

    def get_status_color(self):
        status_color = {
            'to_ship': 'text-muted',
            'in_transit': 'text-warning',
            'delivered': 'text-success'
        }
        return status_color[self.status]