from django.db import models

from apps.users.models import Profile, ProfileAddress, ProfilePayment
from apps.products.models import Product

# Create your models here.
class SaleOrder(models.Model):
    """Model definition for Order."""

    customer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='customer'
    )
    customer_billing_address = models.ForeignKey(
        ProfileAddress,
        related_name='billing_addres',
        on_delete=models.DO_NOTHING,
        limit_choices_to={'profile': customer, 'type': 'billing'}
    )
    customer_shipping_address = models.ForeignKey(
        ProfileAddress,
        related_name='shipping_address',
        on_delete=models.DO_NOTHING,
        limit_choices_to={'profile': customer, 'type': 'shipping'}
    )
    customer_payment = models.ForeignKey(
        ProfilePayment,
        on_delete=models.CASCADE,
        limit_choices_to={'profile': customer}
    )
    seller = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='seller'
    )
    subtotal = models.FloatField()
    total_taxes = models.FloatField()
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
    note = models.TextField()

    class Meta:
        """Meta definition for Order."""

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        """Unicode representation of Order."""
        pass

class SaleOrderLine(models.Model):
    """Model definition for OrderLine."""

    order = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    discount = models.FloatField()
    unit_price = models.FloatField()
    line_total = models.FloatField()


    class Meta:
        """Meta definition for OrderLine."""

        verbose_name = 'Order Line'
        verbose_name_plural = 'Order Lines'

    def __str__(self):
        """Unicode representation of OrderLine."""
        pass
