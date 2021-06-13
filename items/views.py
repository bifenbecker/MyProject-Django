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


# region API View
class SearchItemsAPI(APIView):

    def post(self, request):
        """
        sort: - По какому полю Product сортировать (name, category, created_date, -name, -category, -created_date)
        category: Категория, где искать
        search: Текст поиска
        """

        data = request.data
        sort_by = data['sort']
        search_category = data['category']
        search_product = data['search']

        try:
            try:
                categories = ItemCategory.objects.filter(slug__icontains=search_category)

                if not categories.exists():
                    raise Exception(f"Категория {search_category} не найдена")
            except:
                raise Exception(f"Категория {search_category} не найдена")

            products = Product.objects.none()

            for category in categories:
                print(category.parent)
                add_products = Product.objects.filter(category=category, name__icontains=search_product)

                if add_products.exists():
                    products |= add_products

            if not products.exists():
                raise Exception(f"Продукт {search_product} не найден")

            try:
                products = products.order_by(sort_by)
            except:
                raise Exception(f"Сортировать по {sort_by} невозомжно")

            products_serializer = []
            for product in products:
                product_serializer = ProductSerializer(product)
                products_serializer.append(product_serializer.data)

            return Response({'Result': products_serializer})
        except Exception as e:
            return Response({'Result': str(e)})

# endregion


