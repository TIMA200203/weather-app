from django.urls import path

from reminder.api.v1 import views

app_name = "weather_api"

urlpatterns = [
    path(
        "get-subscription/",
        views.NotificationSubscription.as_view(),
        name="get_subscription",
    ),
    path(
        "update-last-notification-time/",
        views.UpdateLastNotificationTime.as_view(),
        name="update_last_notification_time",
    ),
]
