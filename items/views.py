from .models import *
from .serializer import ProductSerializer

from django.views import View
from django.shortcuts import render
from django.template.defaulttags import register
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

import django.contrib.postgres.search


def search_view(request):
    return render(request, "search.html", context={'items': Item.objects.all()})


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class CategoriesView(View):
    template_name = 'categories.html'

    def get(self, request, *args, **kwargs):
        data = {}
        categories_db = ItemCategory.objects.all()

        for cat_db in categories_db:
            if cat_db.parent == None:
                if cat_db.parent not in data.keys():
                    data[cat_db.name] = []

        for cat_db in categories_db:
            if cat_db.parent != None:
                data[cat_db.parent.name].append(cat_db)
        context = {}
        context['categories'] = data
        return render(request, self.template_name, context=context)


class CategoriesDetailView(View):
    tamplate_name = 'category_detail.html'

    def get(self, request, slug, *args, **kwargs):
        category = get_object_or_404(ItemCategory, slug=slug)
        products = Product.objects.filter(category=category)
        return render(request, self.tamplate_name,context={'category': category, 'products': products})


class SearchItemsAPI(APIView):

    def post(self, request):

        data = request.data
        categories = ItemCategory.objects.filter(parent=not None, name__icontains=data['category'])
        products = []

        for category in categories:
            add_products = Product.objects.filter(category=category, name__icontains=data['search'])

            if add_products.exists():
                products += add_products

        products_serializer = []
        for product in products:
            product_serializer = ProductSerializer(product)
            products_serializer.append(product_serializer.data)


        return Response({'Result': products_serializer})


