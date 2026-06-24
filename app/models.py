from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    middle_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=100, blank=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default="checking")
    currency = models.CharField(max_length=10, choices=CURRENCIES, default="USD")
    occupation = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=30, blank=True)
    profile_image = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    pin = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)  # ✅ editable

    def set_pin(self, raw_pin):
        self.pin = make_password(raw_pin)
        self.save(update_fields=["pin"])

    def check_pin(self, raw_pin):
        if not self.pin:
            return False
        return check_password(raw_pin, self.pin)

    @property
    def has_pin(self):
        return bool(self.pin)

    def __str__(self):
        return f"{self.user.username} Profile"


class WireTransfer(models.Model):
    STATUS_CHOICES = [
        ('Pending',   'Pending'),
        ('Completed', 'Completed'),
        ('Failed',    'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wire_transfers')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    beneficiary_name = models.CharField(max_length=150)
    beneficiary_account_no = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=150)
    country = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=20)
    routing_number = models.CharField(max_length=50, blank=True)
    account_type = models.CharField(max_length=50, blank=True)
    narration = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)  # ✅ editable

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Wire Transfer'
        verbose_name_plural = 'Wire Transfers'

    def __str__(self):
        return f"Wire | {self.user.username} → {self.beneficiary_name} | {self.amount}"


class DomesticTransfer(models.Model):
    STATUS_CHOICES = [
        ('Pending',   'Pending'),
        ('Completed', 'Completed'),
        ('Failed',    'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='domestic_transfers')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    beneficiary_name = models.CharField(max_length=150)
    beneficiary_account_no = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=150)
    account_type = models.CharField(max_length=50, blank=True)
    narration = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)  # ✅ editable

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Domestic Transfer'
        verbose_name_plural = 'Domestic Transfers'

    def __str__(self):
        return f"Domestic | {self.user.username} → {self.beneficiary_name} | {self.amount}"


class LoanApplication(models.Model):
    LOAN_TYPE_CHOICES = [
        ('Personal',  'Personal Loan'),
        ('Business',  'Business Loan'),
        ('Mortgage',  'Mortgage Loan'),
        ('Auto',      'Auto Loan'),
        ('Education', 'Education Loan'),
    ]
    STATUS_CHOICES = [
        ('Pending',  'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    loan_type = models.CharField(max_length=50, choices=LOAN_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    duration_months = models.PositiveIntegerField()
    purpose = models.TextField()
    monthly_income = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)  # ✅ editable

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Loan Application'

    def __str__(self):
        return f"{self.user.username} | {self.loan_type} | {self.amount}"


class Deposit(models.Model):
    DEPOSIT_TYPE_CHOICES = [
        ('DPS',   'Deposit Pension Scheme (DPS)'),
        ('Fixed', 'Fixed Deposit Receipt (FDR)'),
    ]
    STATUS_CHOICES = [
        ('Active',   'Active'),
        ('Matured',  'Matured'),
        ('Closed',   'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    deposit_type = models.CharField(max_length=10, choices=DEPOSIT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    duration_months = models.PositiveIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('5.00'))
    maturity_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(default=timezone.now)  # ✅ editable

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Deposit'

    def __str__(self):
        return f"{self.user.username} | {self.deposit_type} | {self.amount}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)  # ✅ editable

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'

    def __str__(self):
        return f"{self.user.username} | {self.title}"
