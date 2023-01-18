from django import forms
from django.contrib.auth.models import User

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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ProfileAddressForm, self).__init__(*args, **kwargs)

    def save(self):
        data = self.cleaned_data
        address = ProfileAddress(profile=self.request.user.profile, **data)
        address.save()
        return address

class ProfilePaymentForm(forms.ModelForm):
    """Form definition for ProfilePayment."""

    class Meta:
        """Meta definition for ProfilePaymentform."""

        model = ProfilePayment
        fields = (
            'card_number',
            'card_expiration_date'
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ProfilePaymentForm, self).__init__(*args, **kwargs)

    def save(self):
        data = self.cleaned_data
        payment_card = ProfilePayment(profile=self.request.user.profile, **data)
        payment_card.save()
        return payment_card