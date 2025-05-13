from django.db import models
from django.utils import timezone


class Subscription(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    city = models.CharField(max_length=50)

    notification_period = models.PositiveIntegerField(default=24)
    last_notification_time = models.DateTimeField(default=timezone.now)
    is_enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "city")

    def __str__(self):
        return f"{self.user} to {self.city} for {self.notification_period}"
