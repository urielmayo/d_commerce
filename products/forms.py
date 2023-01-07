from itertools import product
from django import forms

from products.models import Product
class ProductForm(forms.ModelForm):
    """Form definition for Product."""

    class Meta:
        """Meta definition for Productform."""

        model = Product
        exclude = ('seller', 'slug')
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ProductForm, self).__init__(*args, **kwargs)

    def clean_sku(self):
        "sku must be unique per product by the same seller"
        sku = self.cleaned_data['sku']
        seller = self.request.user.profile
        if Product.objects.filter(profile=seller, sku=sku).exists():
            raise forms.ValidationError("You already used this sku")
        return sku

    def save(self):
        data = self.cleaned_data
        seller = self.request.user.profile
        slug = Product.create_slug(seller, data['name'])
        product = Product(seller=seller, slug=slug, **data)
        product.save()
        return product