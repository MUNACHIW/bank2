from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


class UserProfile(models.Model):

    ACCOUNT_TYPES = [
        ("checking", "Checking Account"),
        ("savings", "Savings Account"),
        ("business", "Business Account"),
        ("student", "Student Account"),
    ]


    CURRENCIES = [
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
        ("GBP", "British Pound"),
        ("NGN", "Nigerian Naira"),
        ("CAD", "Canadian Dollar"),
        ("AUD", "Australian Dollar"),
    ]


    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )


    middle_name = models.CharField(
        max_length=100,
        blank=True
    )


    phone = models.CharField(
        max_length=30,
        blank=True
    )


    country = models.CharField(
        max_length=100,
        blank=True
    )


    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES,
        default="checking"
    )


    currency = models.CharField(
        max_length=10,
        choices=CURRENCIES,
        default="USD"
    )


    occupation = models.CharField(
        max_length=100,
        blank=True
    )


    street = models.CharField(
        max_length=150,
        blank=True
    )


    city = models.CharField(
        max_length=100,
        blank=True
    )


    state = models.CharField(
        max_length=100,
        blank=True
    )


    zip = models.CharField(
        max_length=30,
        blank=True
    )


    profile_image = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True
    )


    balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00")
    )


    pin = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )


    is_active = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def set_pin(self, raw_pin):

        self.pin = make_password(raw_pin)
        self.save(update_fields=["pin"])



    def check_pin(self, raw_pin):

        if not self.pin:
            return False

        return check_password(
            raw_pin,
            self.pin
        )


    @property
    def has_pin(self):

        return bool(self.pin)


    def __str__(self):

        return f"{self.user.username} Profile"