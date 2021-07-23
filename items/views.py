from items.models import *
from orders.models import Order, ItemToOrder, Stage
from .serializer import *

from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.template.defaulttags import register

from rest_framework.views import APIView
from rest_framework.response import Response


@register.filter
def get_items_qty_in_order(item: Item, order: Order):
    item_to_order = ItemToOrder.objects.filter(item=item, order=order).first()
    return item_to_order.quantity if item_to_order else 0


class SearchView(TemplateView):
    template_name = "search.html"

    @classmethod
    def _get_branch_categories(cls, category: ItemCategory):
        yield category
        if category.child.exists():
            for next_child in category.child.all():
                for child in cls._get_branch_categories(next_child):
                    yield child

    @classmethod
    def _get_parent_categories_path(cls, category: ItemCategory):
        if category.parent:
            for parent in cls._get_parent_categories_path(category.parent):
                yield parent
        yield category

    def get_context_data(self, **kwargs):
        slug = kwargs.get('slug', None)
        products = Product.objects.all()
        if slug:
            search_category = get_object_or_404(ItemCategory, slug=slug)
            products = products.filter(category__in=self._get_branch_categories(search_category))
        else:
            search_category = None

        return {
            'page_title': settings.PAGE_TITLE_PREFIX + 'Товары' + (' - ' + search_category.name if search_category else ''),
            'toolbar_title': 'Категория: ' + search_category.name if search_category else 'Товары',
            'products': products,
            'current_category_name': search_category.name if search_category else 'Категории',
            'child_categories': search_category.child.all() if search_category else ItemCategory.objects.filter(parent__isnull=True),
            'parent_category_path': list(self._get_parent_categories_path(search_category))[:-1] if search_category else []
        }


class ProductDetailsView(TemplateView):
    template_name = "product_details.html"

    def get_context_data(self, **kwargs):
        product = get_object_or_404(Product, id=kwargs['product_id'])
        return {
            'page_title': settings.PAGE_TITLE_PREFIX + product.name,
            'toolbar_title': product.name,
            'product': product,
            'active_order': self.request.user.get_active_order()
        }


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


class SetItemStageAPI(APIView):

    def post(self, request):
        item_to_order = ItemToOrder.objects.get(id=request.data['item_to_order_id'])
        product_stage_name = request.data['product_stage_id'].split('_')[0]
        product_stage_id = request.data['product_stage_id'].split('_')[1]
        stage = Stage.objects.get(id=product_stage_id, name=product_stage_name)
        item_to_order.set_stage(stage)
        return Response({'Result': 'OK'})


class GetSimilarsAPI(APIView):

    def get(self, request):
        similars = []
        try:
            item_to_order_item_id = request.GET.get('item_to_order_item_id')
            item = Item.objects.get(id=item_to_order_item_id)
            for similar_product in item.product.similar.all():
                item = {}
                for similar in similar_product.items.all():
                    item['id'] = similar.id
                    item['name'] = similar.name
                    item['supplier'] = similar.supplier.name
                    item['unit_measurement'] = UNIT_MEASUREMENT_CHOICES[similar.unit_measurement][1]
                similars.append(item)
            return Response({'similars': similars})
        except:
            return Response({'error': 'Не удалось найти аналоги'})
