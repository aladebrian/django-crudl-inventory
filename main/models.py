from django.db import models
import uuid
# Create your models here.

class User(models.Model):
    USER_TYPES = [("customer", "Customer"), ("seller", "Seller"), ("admin", "Admin")]
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=200)
    user_type = models.CharField(max_length=30, choices=USER_TYPES, default="customer")

    def __str__(self):
        return self.user_name
    
class Category(models.Model):
    category_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()

class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=8)
    quantity = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="related seller", editable=False)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="related category")
    