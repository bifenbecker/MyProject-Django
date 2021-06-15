from rest_framework import serializers
from .models import ItemToOrder


class ItemToOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemToOrder
        fields = ['item', 'order', 'quantity']