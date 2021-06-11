from django.core.management.base import BaseCommand
from items.models import Supplier, ItemCategory, Item, Product


class Command(BaseCommand):
    help = 'Fills database with test data'

    def handle(self, *args, **options):
        Item.objects.all().delete()
        Supplier.objects.all().delete()
        ItemCategory.objects.filter(parent__isnull=False).delete()
        ItemCategory.objects.all().delete()

        sup1 = Supplier.objects.get_or_create(name='Эльдорадо')[0]
        sup2 = Supplier.objects.get_or_create(name='Mile')[0]
        sup3 = Supplier.objects.get_or_create(name='Oma')[0]

        ic1 = ItemCategory.objects.get_or_create(name='Стройматериалы')[0]
        ic2 = ItemCategory.objects.get_or_create(name='Цемент', parent=ic1)[0]
        ic3 = ItemCategory.objects.get_or_create(name='Доски', parent=ic1)[0]

        product1 = Product.objects.get_or_create(name='Доска', category=ic3, supplier=sup1)
        product2 = Product.objects.get_or_create(name='Цемент', category=ic2, supplier=sup3)


        for i in range(2, 20):
            Item.objects.create(name='Цемент ' + str(i * 10), product=product2[0], unit_measurement=8)

        for i in range(2, 15):
            Item.objects.create(name='Доска дубовая 10x' + str(i * 10), product=product1[0], unit_measurement=2)

        for i in range(2, 15):
            Item.objects.create(name='Доска из клена 10x' + str(i * 10), product=product1[0], unit_measurement=2)
