from django.contrib import admin
from .models import UserProfile, WireTransfer, DomesticTransfer , LoanApplication ,Deposit,  Notification


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone",
        "country",
        "account_type",
        "currency",
        "balance",
        "is_active",
        "created_at",
    )

    list_filter = (
        "account_type",
        "currency",
        "country",
        "is_active",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "phone",
        "country",
    )

  
    list_editable = ( "balance", "created_at",)
    
@admin.register(WireTransfer)
class WireTransferAdmin(admin.ModelAdmin):
    list_display = ("user", "beneficiary_name", "bank_name", "amount", "country", "swift_code", "status", "created_at")
    search_fields = ("user__username", "beneficiary_name", "bank_name", "swift_code")
    list_filter = ("status", "country", "created_at")
    ordering = ("-created_at",)
    list_editable = ("status", "created_at")
  


@admin.register(DomesticTransfer)
class DomesticTransferAdmin(admin.ModelAdmin):
    list_display = ("user", "beneficiary_name", "bank_name", "amount", "status", "created_at")
    search_fields = ("user__username", "beneficiary_name", "bank_name")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)
    list_editable = ("status", "created_at")
    
    

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'loan_type', 'amount', 'duration_months', 'status', 'created_at')
    list_filter  = ('loan_type', 'status', 'created_at')
    search_fields = ('user__username', 'purpose')
    ordering = ('-created_at',)

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display  = ('user', 'deposit_type', 'amount', 'duration_months', 'interest_rate', 'status', 'maturity_date', 'created_at')
    list_filter   = ('deposit_type', 'status', 'created_at')
    search_fields = ('user__username',)
    ordering      = ('-created_at',)
    list_editable = ("created_at",)
    
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display  = ('user', 'title', 'is_read', 'created_at')
    list_filter   = ('is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    ordering      = ('-created_at',)



