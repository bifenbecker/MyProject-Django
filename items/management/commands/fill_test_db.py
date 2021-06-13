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
        ic2 = ItemCategory.objects.get_or_create(name='Краски', parent=ic1)[0]

        product1 = Product.objects.get_or_create(name='Фасадные краски', category=ic2)[0]
        product2 = Product.objects.get_or_create(name='Краски для наружных работ', category=ic2)[0]
        product3 = Product.objects.get_or_create(name='Доски', category=ic1)[0]


        for i in range(2, 5):
            Item.objects.create(name='Краска ' + str(i), product=product1, unit_measurement=8, supplier=sup1)

        for i in range(5, 11):
            Item.objects.create(name='Краска ' + str(i), product=product2, unit_measurement=2, supplier=sup3)

        for i in range(3, 6):
            Item.objects.create(name='Доска из клена 10x' + str(i * 10), product=product3, unit_measurement=2, supplier=sup2)
