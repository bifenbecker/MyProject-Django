from django.contrib import admin
from django.urls import path, include


handler404 = 'home.views.handle_404_view'


urlpatterns = [
    path('pilaru/', include([
        path('admin/', admin.site.urls),
        path('', include('home.urls')),
        path('accounts/', include('accounts.urls')),
        path('items/', include('items.urls'))
    ])),
]
