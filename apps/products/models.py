from decimal import Decimal
from django.utils.text import slugify
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from apps.products.validators import validate_image_size
from apps.users.models import Profile
# Create your models here.
class ProductCategory(models.Model):
    """Model definition for ProductCategory."""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True)
    class Meta:
        """Meta definition for ProductCategory."""

        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        """Unicode representation of ProductCategory."""
        return self.name


class Brand(models.Model):
    """Model definition for Brand."""

    # TODO: Define fields here
    name = models.CharField(max_length=100)

    class Meta:
        """Meta definition for Brand."""

        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        """Unicode representation of Brand."""
        return self.name


class Product(models.Model):
    """Model definition for Product."""

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(ProductCategory)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sku = models.CharField(max_length=20)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.TextField(blank=True)
    stock_qty = models.PositiveIntegerField()
    slug = models.SlugField(unique=True)
    picture = models.ImageField(
        upload_to='product_pics',
        validators=[validate_image_size],
        null=True
    )

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def in_stock(self):
        return self.stock_qty > 0

    def __str__(self):
        """Unicode representation of Product."""
        return self.name

    def get_categories(self):
        return self.categories.all()
    @staticmethod
    def create_slug(seller, product_name):
        product_slug = slugify(product_name).lower()
        return f'{seller.pk}-{product_slug}'

    @staticmethod
    def get_product_set_categories(products):
        categories = set()
        for product in products:
            for category in product.categories.all():
                categories.add(category)
        return categories


class Attribute(models.Model):
    """Model definition for Attribute."""

    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(max_length=20)

    class Meta:
        """Meta definition for Attribute."""

        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'

    def __str__(self):
        """Unicode representation of Attribute."""
        return self.name

class AttributeValue(models.Model):
    """Model definition for AttributeValue."""

    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

    class Meta:
        """Meta definition for AttributeValue."""

        verbose_name = 'Attribute Value'
        verbose_name_plural = 'Attribute Values'

    def __str__(self):
        """Unicode representation of AttributeValue."""
        return self.value

class ProductQuestion(models.Model):
    """Model definition for ProductQuestion."""

    # TODO: Define fields here
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    questioner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='questioner'
    )
    responder = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='responder'
    )
    question = models.TextField()
    answer = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for ProductQuestion."""

        verbose_name = 'Product Question'
        verbose_name_plural = 'Product Questions'
        ordering = ['-pub_date']

class ProductReview(models.Model):
    """Model definition for ProductReview."""

    # TODO: Define fields here
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    score = models.SmallIntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=False)

    class Meta:
        """Meta definition for ProductReview."""
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'reviewer'],
                name='unique_product_review'
            )
        ]
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        ordering = ['-pub_date']
