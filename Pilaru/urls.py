from django.contrib import admin
from django.urls import path, include


handler404 = 'home.views.handle_404_view'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('items/', include('items.urls')),
    path('orders/', include('orders.urls'), name='order_url'),
]
