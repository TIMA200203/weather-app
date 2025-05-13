from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from subscription.models import Subscription
from users.models import User


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (SubscriptionInline,)

    list_display = (
        "email",
        "username",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
        "updated_at",
    )
    search_fields = ("email", "username")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    ordering = ("-created_at",)
    readonly_fields = ("last_login",)
