from django import forms
from django.forms.models import inlineformset_factory

from apps.products.models import Product, Attribute
class ProductForm(forms.ModelForm):
    """Form definition for Product."""

    class Meta:
        """Meta definition for Productform."""

        model = Product
        exclude = ('seller', 'slug', 'picture')
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_qty': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ProductForm, self).__init__(*args, **kwargs)

    def clean_sku(self):
        "sku must be unique per product by the same seller"
        sku = self.cleaned_data['sku']
        seller = self.request.user.profile
        if Product.objects.filter(seller=seller, sku=sku).exists():
            raise forms.ValidationError("You already used this sku")
        return sku

    def save(self):
        data = self.cleaned_data
        print(data)
        categories = data.pop('categories')
        seller = self.request.user.profile
        slug = Product.create_slug(seller, data['name'])
        product = Product.objects.create(seller=seller, slug=slug, **data)
        for category in categories:
            product.categories.add(category)
        product.save()
        return product

class AttributeForm(forms.ModelForm):
    """Form definition for Attribute."""

    class Meta:
        """Meta definition for Attributeform."""

        model = Attribute
        exclude = ('product', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Name'}),
            'value': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Value'})
        }


AttributeFormSet = inlineformset_factory(
    Product,
    Attribute,
    form=AttributeForm,
    min_num=3,
    validate_min=True,
    extra=3,
    can_delete=False
)