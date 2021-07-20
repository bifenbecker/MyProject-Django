from django.urls import path, include
from .views import *


urlpatterns = [
    path('search/', SearchView.as_view(), name='search_url'),
    path('search/<slug>', SearchView.as_view(), name='search_category_url'),
    path('view/<int:product_id>', ProductDetailsView.as_view(), name='product_details_url'),
    # path('api/search_items', SearchItemsAPI.as_view()),
    path('api/set_stage', SetItemStageAPI.as_view()),
]
