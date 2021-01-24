from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import ValidationToken


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    list_display = (
        'email', 'phone_number', 'full_name', 'admin', 'staff', 'email_verified', 'phone_number_verified', 'active')
    list_filter = ('admin', 'staff', 'email_verified', 'phone_number_verified', 'active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
         {'fields': ('first_name', 'last_name', 'phone_number', 'email_verified', 'phone_number_verified')}),
        ('Permissions', {'fields': ('active', 'staff', 'admin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'phone_number', 'full_name',)
    ordering = ('email',)
    filter_horizontal = ()


class ValidationTokenAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'token', 'validation_type', 'create_date', 'is_expired',)
    list_filter = ('validation_type',)
    search_fields = ('user', 'token', 'validation_type',)
    ordering = ('user',)
    fields = ('user', 'token', 'validation_type', 'create_date', 'is_expired',)
    readonly_fields = ('create_date', 'is_expired',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(ValidationToken, ValidationTokenAdmin)