from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'full_name', 'telegram_id',
                    'confirm_code', 'created_at', 'is_staff')
    search_fields = ('phone_number', 'full_name', 'telegram_id')
    list_per_page = 100
