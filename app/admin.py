from django.contrib import admin
from .models import UserProfile


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

    readonly_fields = (
        "created_at",
        "balance",
    )