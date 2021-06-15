from rest_framework import serializers
from .models import Product, Item

class ProductSerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField('get_items_count')

    def get_items_count(self, product):
        return Item.objects.filter(product=product).count()

    class Meta:
        model = Product
        fields = ['name', 'id', 'items_count']

