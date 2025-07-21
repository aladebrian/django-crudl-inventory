from django.db import models
from django.utils import timezone
# from registration.models import CustomUser
import uuid
# Create your models here.
    
class Category(models.Model):
    category_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField()

class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    # seller_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="related seller")
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="related category")
    