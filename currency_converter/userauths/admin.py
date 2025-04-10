from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'first_name', 'last_name', 'email', 'balance_usd', 'balance_gbp', 'is_active')
    list_filter = ('account_usd', 'account_gbp')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Balances', {'fields': ('balance_usd', 'balance_gbp')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email', 'account_usd', 'account_gbp')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)