from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    secondary_street = models.CharField(max_length=100)
    zip_code = models.PositiveSmallIntegerField()
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)


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
