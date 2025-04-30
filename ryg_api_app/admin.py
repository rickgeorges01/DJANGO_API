from django.contrib import admin

from ryg_api_app.models import Product,UserPermission

# Register your models here.
admin.site.register(Product)
admin.site.register(UserPermission)