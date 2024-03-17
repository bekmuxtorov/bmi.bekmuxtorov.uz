from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(
        verbose_name="Phone number",
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\+998\d{9}$',
                message='Invalid phone number. Please enter in the format +998901234567'
            )
        ]
    )
    telegram_id = models.CharField(
        verbose_name="Telegam ID",
        max_length=21,
        blank=True
    )
    full_name = models.CharField(
        verbose_name="Full Name",
        max_length=100,
    )
    confirm_code = models.IntegerField(
        verbose_name="Confirm code",
        blank=True,
        null=True
    )
    is_staff = models.BooleanField(
        verbose_name="is staff",
        default=False
    )
    daily_use = models.IntegerField(
        verbose_name="Kunlik foydalanish imkoniyati",
        null=True,
        blank=True,
        default=2
    )
    created_at = models.DateTimeField(
        verbose_name="Created time",
        auto_now_add=True
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def __str__(self):
        return self.full_name
