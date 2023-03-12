from django import forms
from django.forms.models import inlineformset_factory

from apps.products.models import Product, Attribute, ProductReview
class ProductForm(forms.ModelForm):
    """Form definition for Product."""

    class Meta:
        """Meta definition for Productform."""

        model = Product
        exclude = ('seller', 'slug')
        widgets = {
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_qty': forms.NumberInput(attrs={'class': 'form-control'}),
            'condition': forms.RadioSelect()
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

class ProductReviewForm(forms.ModelForm):
    """Form definition for ProductReview."""

    class Meta:
        """Meta definition for ProductReviewform."""

        model = ProductReview
        fields = ('score', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        self.reviewer = kwargs.pop('reviewer')
        self.order_line = kwargs.pop('order_line')
        super(ProductReviewForm, self).__init__(*args, **kwargs)

    def save(self):
        data = self.cleaned_data
        review = ProductReview(
            reviewer=self.reviewer,
            product=self.order_line.product,
            order_line=self.order_line,
            **data
        )
        review.save()
        return review

