from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['user_id', 'user_name', 'user_type', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('user_id', 'user_name', 'password', 'user_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'user_name', 'user_type', 'password1', 'password2'),
        }),
    )
    search_fields = ('user_name',)
    ordering = ('user_id',)

admin.site.register(CustomUser, CustomUserAdmin)
