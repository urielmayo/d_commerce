from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

from datetime import date
from dateutil.relativedelta import relativedelta

from apps.users.models import Profile, ProfileAddress, ProfilePayment, ShoppingCart
class SignUpForm(forms.Form):

    username = forms.CharField(
        min_length=4,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_confirmation = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        """username must be unique"""
        username = self.cleaned_data['username']
        username_exists = User.objects.filter(username=username).exists()

        if username_exists:
            raise forms.ValidationError('Username already Taken')
        return username

    def clean(self):
        """verifies password confirmation"""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match')

        return data

    def save(self):
        """create user in database"""
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()
        cart = ShoppingCart.objects.create(profile=profile)

class ProfileAddressForm(forms.ModelForm):
    """Form definition for ProfileAddress."""

    class Meta:
        """Meta definition for ProfileAddressform."""

        model = ProfileAddress
        exclude = ('profile', )
        widgets = {
            'main_street': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Main Street'}
            ),
            'number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Number'}
            ),
            'secondary_street': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Secondary Street'}
            ),
            'notes': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'References'}
            ),
            'zip_code': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'ZIP Code'}
            ),
            'city': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'City'}
            ),
            'state': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'State'}
            ),
            'country': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Country'}
            ),
            'type': forms.RadioSelect()
        }

class ProfilePaymentForm(forms.ModelForm):
    """Form definition for ProfilePayment."""

    class Meta:
        """Meta definition for ProfilePaymentform."""

        model = ProfilePayment
        fields = (
            'card_number',
            'card_expiration_month',
            'card_expiration_year',
        )
        widgets = {
            'card_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'XXXX XXXX XXXX XXXX'}
            ),
            'card_expiration_month': forms.Select(
                choices=[(i, i) for i in range(1, 13)],
                attrs={'class': 'form-control'}
            ),
            'card_expiration_year': forms.Select(
                choices=[(i, i) for i in range(date.today().year, date.today().year + 30)],
                attrs={'class': 'form-control'}
            ),
        }

    def clean(self):
        cleaned_data =  super().clean()

        month = cleaned_data['card_expiration_month']
        year = cleaned_data['card_expiration_year']
        # we ensure that the expration date is valid
        last_card_expiration_day = date(year, month, 1) + relativedelta(days=31)
        if date.today() > last_card_expiration_day:
            raise ValidationError(
                "Expiration date is outdated"
            )

        return cleaned_data