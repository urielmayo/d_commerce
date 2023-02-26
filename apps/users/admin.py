from django.contrib import admin

from apps.users.models import Profile, ProfileAddress, ShoppingCart, ProfilePayment
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''Admin View for Profile'''

@admin.register(ProfileAddress)
class ProfileAddressAdmin(admin.ModelAdmin):
    '''Admin View for Profile Address'''

@admin.register(ProfilePayment)
class ProfilePaymentAdmin(admin.ModelAdmin):
    '''Admin View for Profile Address'''

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    '''Admin View for Profile Shopping Cart'''