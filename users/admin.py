from django.contrib import admin

from users.models import Profile, ProfileAddress, ProfilePayment
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''Admin View for Profile'''

@admin.register(ProfileAddress)
class ProfileAddressAdmin(admin.ModelAdmin):
    '''Admin View for Profile Address'''