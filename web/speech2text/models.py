from django.db import models
from accounts.models import User


class Attempt(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name="attempts",
        verbose_name="Foydalanuvchi",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    audio = models.FileField(
        verbose_name="audio",
        upload_to="audios/",
        null=True,
        blank=True
    )
    audio_code = models.IntegerField(
        verbose_name="Audio code",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ' | '.join(['Audio', str(self.id), self.user.full_name])
