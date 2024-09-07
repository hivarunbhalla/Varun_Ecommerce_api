from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin, ProductImageInline
from store.models import Product
from tags.models import TaggedItem
from .models import User


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    extra = 1

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline, ProductImageInline] 
    list_filter = ('unit_price', 'last_update')

class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'email', 'first_name', 'last_name'),
            },
        ),
    )
    pass

admin.site.unregister(Product)  #removing old model from admin site
admin.site.register(Product, CustomProductAdmin)
admin.site.register(User, UserAdmin)

