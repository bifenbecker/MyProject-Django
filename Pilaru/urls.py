from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


handler404 = 'home.views.handle_404_view'


urlpatterns = [
    path('pilaru/', include([
        path('admin/', admin.site.urls),
        path('', include('home.urls')),
        path('accounts/', include('accounts.urls')),
        path('items/', include('items.urls')),
        path('orders/', include('orders.urls'), name='order_url'),
        path('project/', include('projects.urls'), name='projects_url'),
    ] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) if settings.IS_LOCAL_DEV else []))),
]
