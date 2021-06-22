from django.core.management.base import BaseCommand
from django.db.models.deletion import ProtectedError
from items.models import Supplier, ItemCategory, Item, Product
from orders.models import Stage, OrderState, OrderStateToOrder, Order, PriceOffer
import random


class Command(BaseCommand):
    help = 'Fills database with test data'

    def handle(self, *args, **options):
        Item.objects.all().delete()
        Supplier.objects.all().delete()
        Product.objects.all().delete()
        Stage.objects.all().delete()
        OrderStateToOrder.objects.all().delete()
        OrderState.objects.all().delete()
        Order.objects.all().delete()
        PriceOffer.objects.all().delete()
        while ItemCategory.objects.all().exists():
            for ic in ItemCategory.objects.all():
                try:
                    ic.delete()
                except ProtectedError:
                    pass

        with open('test_data.tsv', 'r', encoding='utf-8') as f:
            data = f.readlines()

        data.pop(0)
        data.pop(0)
        data = [row.split('\t') for row in data]

        ic_other = ItemCategory.objects.get_or_create(name='Другое')[0]

        suppliers_names = ('Сатурн', 'Планета электрика', 'Стройкомплект', 'Очаг', 'Магазин', 'Современные окна', 'Дострой', )
        suppliers = [Supplier.objects.get_or_create(name=name)[0] for name in suppliers_names]

        for order_state_name in ('Активный', 'Закрыт', ):
            OrderState.objects.create(name=order_state_name)

        for row in data:
            print(row)

            # create categories if all 3 lvls specified
            if (len(row[2]) > 2) and (len(row[3]) > 2) and (len(row[4]) > 2):
                ic = ItemCategory.objects.get_or_create(
                    name=row[4].strip(),
                    parent=ItemCategory.objects.get_or_create(
                        name=row[3].strip(),
                        parent=ItemCategory.objects.get_or_create(name=row[2].strip())[0]
                    )[0]
                )[0]
            else:
                ic = ic_other

            p = Product.objects.create(
                name=row[1].strip(),
                category=ic,
                unit_measurement=2
            )

            for supplier in suppliers:
                if random.random() > 0.5:
                    Item.objects.create(
                        name=row[1].strip(),
                        supplier=supplier,
                        product=p,
                        unit_measurement=2
                    )

            if len(row[5]) > 2:
                Stage.objects.get_or_create(name=row[5].strip())
