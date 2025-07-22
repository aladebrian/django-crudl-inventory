from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission, BaseUserManager
from django.utils import timezone

def next_user_id():
    """Generate a unique ID for the user."""
    last_user = CustomUser.objects.order_by('user_id').last()
    return last_user.user_id + 1 if last_user else 1

class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, user_id=None,user_type=None, password=None):
        
        if not user_name:
            raise ValueError("Users must have a user_name")
        if not user_type:
            user_type = "customer"
        if not user_id:
            user_id = next_user_id()
        user = self.model(
            user_id=user_id,
            user_name=user_name,
            user_type=user_type,
        )
        if user_type == "admin":
            user.is_staff = True
            user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, user_id=None,  user_type='admin', password=None):
        user = self.create_user(
            user_id=user_id,
            user_name=user_name,
            user_type=user_type,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = [("customer", "Customer"), ("seller", "Seller"), ("admin", "Admin")]
    user_id = models.IntegerField(primary_key=True, default=next_user_id)
    user_name = models.CharField(max_length=40, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default="customer")
    is_staff = models.BooleanField(default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        verbose_name=_('groups'),
        help_text=_('The groups this user belongs to.'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        verbose_name=_('user permissions'),
        help_text=_('Specific permissions for this user.'),
    )   

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
    
    def __str__(self):
        return str(self.user_name)