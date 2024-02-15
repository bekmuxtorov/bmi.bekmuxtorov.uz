from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    phone_number_validator = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Invalid phone number. Please enter in the format +998901234567"
    )

    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError(_("The phone number must be set"))

        if self.phone_number_validator(phone_number):
            raise ValueError(
                'Invalid phone number. Please enter in the format +998909234567')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(
            phone_number=phone_number,
            password=password,
            **extra_fields
        )
