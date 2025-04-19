from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    # API endpoints
    path('api/labour/', include('labour.urls', namespace='labour')),
    path('api/transactions/', include('transactions.urls', namespace='transactions')),
    path('api/reports/', include('reports.urls', namespace='reports')),
    path('api/vendors/', include('vendors.urls')),  # Added vendors API routes
    path('reports/', include('reports.urls', namespace='reports')),  # Include reports URLs at both paths
    path('users/', include('users.urls', namespace='users')),
    path('logout/', RedirectView.as_view(url='/users/logout/', permanent=False)),
    path('logout', RedirectView.as_view(url='/users/logout/', permanent=False)),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
