from django.urls import path

from subscription.api.v1 import views

app_name = "subscription_api"

urlpatterns = [
    path("create", views.SubscriptionAPI.as_view(), name="create"),
    path(
        "<int:subscription_id>/edit",
        views.SubscriptionAPI.as_view(),
        name="edit",
    ),
    path(
        "<int:subscription_id>/delete",
        views.SubscriptionAPI.as_view(),
        name="delete",
    ),
    path("list/<str:username>", views.SubscriptionList.as_view(), name="list"),
    path(
        "<int:subscription_id>/disable",
        views.DisableSubscription.as_view(),
        name="disable",
    ),
    path(
        "<int:subscription_id>/enable",
        views.EnableSubscription.as_view(),
        name="enable",
    ),
]
