from django.contrib import admin

from apps.orders.models import Order, OrderLine
# Register your models here.

class OrderLineTabularInline(admin.TabularInline):
    model = OrderLine

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''

    inlines = [
        OrderLineTabularInline,
    ]