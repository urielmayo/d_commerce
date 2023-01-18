from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist

# Create your models here.
class Profile(models.Model):
    """Model definition for Profile."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    picture = models.ImageField(
        upload_to='users/pictures',
        blank=True,
        null=True
    )

    class Meta:
        """Meta definition for Profile."""

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Unicode representation of Profile."""
        return self.user.username

class ProfileAddress(models.Model):
    """Model definition for ProfileAddress."""

    # TODO: Define fields here
    type = models.CharField(
        choices=[
            ('shipping', 'Shipping'),
            ('billing', 'Billing')
        ],
        default='shipping',
        max_length=20
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    main_street = models.CharField(max_length=100)
    number = models.PositiveSmallIntegerField()
    secondary_street = models.CharField(max_length=100, blank=True)
    zip_code = models.PositiveSmallIntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    notes = models.TextField(blank=True)


    class Meta:
        """Meta definition for ProfileAddress."""

        verbose_name = 'Profile Address'
        verbose_name_plural = 'Profile Addresses'

    def __str__(self):
        """Unicode representation of ProfileAddress."""
        return f'{self.main_street} {self.number}'

def only_numbers(value):
    if not value.isdigit():
        raise ValidationError('credit card containt non-numeric characters')

class ProfilePayment(models.Model):
    """Model definition for ProfilePayment."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    card_number = models.CharField(
        max_length=16,
        unique=True,
        validators=[only_numbers,],
    )
    card_expiration_date = models.CharField(max_length=5)

    class Meta:
        """Meta definition for ProfilePayment."""

        verbose_name = 'Profile Payment'
        verbose_name_plural = 'Profile Payments'

class ShoppingCart(models.Model):
    """Model definition for ShoppingCart."""

    # TODO: Define fields here
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    @property
    def total(self):
        return sum([l.line_total for l in self.shopping_cart_lines.all()])

    class Meta:
        """Meta definition for ShoppingCart."""

        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'

    def is_empty(self):
        return self.shopping_cart_lines.all().count() == 0

    def __str__(self):
        return f"{self.profile}'s shopping cart"

    def add_item(self, product):
        try:
            product_cart_line = self.shopping_cart_lines.get(product=product)
            product_cart_line.quantity += 1
            product_cart_line.save()
        except ObjectDoesNotExist:
            self.shopping_cart_lines.create(product=product)

class ShoppingCartLine(models.Model):
    """Model definition for ShoppingCartLine."""

    shpping_cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name='shopping_cart_lines'
    )
    product = models.OneToOneField('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    @property
    def line_total(self):
        return self.product.price * self.quantity

    class Meta:
        """Meta definition for ShoppingCartLine."""
        verbose_name = 'Shopping Cart Line'
        verbose_name_plural = 'Shopping Cart Lines'

    def __str__(self):
        """Unicode representation of ShoppingCartLine."""
        return f'scl: {self.product.name} [{self.quantity}]'
