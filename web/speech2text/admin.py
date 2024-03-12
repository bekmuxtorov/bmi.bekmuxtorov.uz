from django.contrib import admin
from .models import Attempt


@admin.register(Attempt)
class AttemptModel(admin.ModelAdmin):
    list_display = ("user", "audio", "audio_code", "created_at")
    search_fields = ("user__full_name", "user__telegram_id",
                     "user__phone_number")
    list_filter = ("user",)
