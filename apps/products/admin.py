from itertools import product
from django.contrib import admin
from apps.products.models import (
    ProductCategory,
    Brand,
    Product,
    Attribute,
    ProductQuestion,
    ProductReview
)

class AttributeInline(admin.TabularInline):
    '''Tabular Inline View for '''
    model = Attribute

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''Admin View for Product'''
    inlines = [AttributeInline, ]

@admin.register(ProductQuestion)
class ProductQuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    pass
