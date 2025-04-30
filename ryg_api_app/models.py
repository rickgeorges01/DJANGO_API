from django.db import models
from django.contrib.auth.models import User

class UserPermission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_view_products = models.BooleanField(default=False)
    can_add_products = models.BooleanField(default=False)
    can_update_products = models.BooleanField(default=False)
    can_access_top10 = models.BooleanField(default=False)

    def __str__(self):
        return f"Droits de {self.user.username}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
