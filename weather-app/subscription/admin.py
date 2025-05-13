from django.contrib import admin

from subscription.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "city",
        "notification_period",
        "last_notification_time",
        "is_enabled",
        "created_at",
        "updated_at",
    )
    list_filter = ("user", "city", "is_enabled")
    search_fields = ("user", "city")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
