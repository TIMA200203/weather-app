# core/urls.py

from django.contrib import admin
from django.urls import include, path
from reminder.api.v1 import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="Документація API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/v1/', include('users.api.v1.urls', namespace='auth_api')),
    path('api/weather-data/v1/', include('reminder.api.v1.urls', namespace='weather_api')),
    path('api/subscription/v1/', include('subscription.api.v1.urls', namespace='subscription_api')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('', include('main.urls', namespace='main')),
    path('subscriptions/', include('subscription.urls', namespace='subscription')),
    path('users/', include('users.urls', namespace='users')),
]
