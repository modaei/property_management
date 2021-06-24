from django.contrib import admin
from django.urls import path, include
from .views import media_access

urlpatterns = [
    # Django Admin console.
    path('admin/', admin.site.urls),

    # Media files serving and access management
    path('media/<str:filename>/', media_access, name='media'),
    path('media/<str:media_type>/<str:filename>/', media_access, name='media'),

    # APIs for user accounts management.
    path('api/accounts/', include('accounts.api.urls')),

    # APIs for accessing geographical data such as world countries and cities.
    path('api/geography/', include('geography.api.urls')),

    # APIs for managing properties
    path('api/properties/', include('properties.api.urls')),

    # APIs for managing rental contracts and tenants
    path('api/rents/', include('rents.api.urls')),
]
