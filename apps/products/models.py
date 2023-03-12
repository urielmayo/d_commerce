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
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        """Meta definition for Brand."""

        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        ordering = ['name']

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
    condition = models.CharField(
        choices=[
            ('new', 'New'),
            ('used', 'Used'),
            ('refurbished', 'Refurbished')
        ],
        default='new',
        max_length=15
    )

    @property
    def avg_score(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(reviews.values_list('score', flat=True)) / reviews.count(), 1)

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def in_stock(self):
        return self.stock_qty > 0

    def __str__(self):
        """Unicode representation of Product."""
        return self.name

    def get_reviews_by_score(self):
        """Get a dicttionary like this:
        Key: score of the review (from 1 to 5)
        Value: Number of review with this score
        """
        count = self.reviews.all().count()
        if not count:
            return {k: 0 for k in range(1,6)}
        return {k: self.reviews.filter(score=k).count() / count * 100  for k in range(1,6)}

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    value = models.CharField(max_length=20)

    class Meta:
        """Meta definition for Attribute."""

        verbose_name = 'Attribute'
        verbose_name_plural = 'Attributes'

    def __str__(self):
        """Unicode representation of Attribute."""
        return self.name

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
    pub_date = models.DateTimeField(auto_now_add=True)
    order_line = models.OneToOneField(
        'orders.OrderLine',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        """Meta definition for ProductReview."""
        constraints = [
            models.UniqueConstraint(
                fields=['order_line', 'reviewer'],
                name='unique_product_review'
            )
        ]
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        ordering = ['-pub_date']
