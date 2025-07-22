from django.db import models
from django.utils import timezone
from account.models import CustomUser
import uuid
# Create your models here.
def next_category_id():
    """Generate a unique ID for the category."""
    last_category = Category.objects.order_by('category_id').last()
    return last_category.category_id + 1 if last_category else 1
class Category(models.Model):
    category_id = models.IntegerField(primary_key=True, default=next_category_id)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()

class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    seller_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="related seller", default=None)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="related category")
    