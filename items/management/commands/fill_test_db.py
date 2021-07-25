from django.core.management.base import BaseCommand
from django.db.models.deletion import ProtectedError
from django.contrib.auth import get_user_model
from items.models import Supplier, ItemCategory, Item, Product
from orders.models import Stage, OrderState, OrderStateToOrder, Order, PriceOffer, ItemToOrder
from projects.models import *
import datetime
import random


User = get_user_model()
TEST_USER_CREDS = ('test@gmail.com', '12345678')


def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


class Command(BaseCommand):
    help = 'Fills database with test data'

    def handle(self, *args, **options):
        # === CLEAN ===
        ItemToOrder.objects.all().delete()
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

        # === CREATE TEST USER ===
        test_user = User.objects.filter(email=TEST_USER_CREDS[0]).first()
        if test_user is not None:
            test_user.delete()
        test_user = User.objects.create_user(
            username=TEST_USER_CREDS[0],
            email=TEST_USER_CREDS[0],
            password=TEST_USER_CREDS[1]
        )

        # === READ FILE DATA ===
        with open('test_data.tsv', 'r', encoding='utf-8') as f:
            data = f.readlines()

        data.pop(0)
        data.pop(0)
        data = [row.split('\t') for row in data]

        ic_other = ItemCategory.objects.get_or_create(name='Другое')[0]

        # === FILL DATABASE ===
        suppliers_names = ('Сатурн', 'Планета электрика', 'Стройкомплект', 'Очаг', 'Магазин', 'Современные окна', 'Дострой', )
        suppliers = [Supplier.objects.get_or_create(name=name)[0] for name in suppliers_names]

        order_states = {}
        for order_state_name in ('Активный', 'Завершен', 'Отменен'):
            order_states[order_state_name] = OrderState.objects.create(name=order_state_name)

        all_items = list()
        all_stages = list()
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
                    item = Item.objects.get_or_create(
                        name=row[1].strip(),
                        supplier=supplier,
                        product=p,
                        unit_measurement=2
                    )[0]
                    all_items.append(item)

            if len(row[5]) > 2:
                stage = Stage.objects.get_or_create(name=row[5].strip())[0]
                all_stages.append(stage)

        for product in Product.objects.all():
            product.similar.add(random.choice(Product.objects.all()))

        # === CREATE TEST PROJECTS ===
        all_projects = list()
        for project_name in ('д. Далеково, 13', 'ул. Варнавы 3', 'д.Волошина, 13б'):
            project = Project.objects.get_or_create(name=project_name)[0]
            ProjectMember.objects.create(
                user=test_user,
                access=0,
                project=project
            )
            all_projects.append(project)

        # === FILL ORDERS ===
        items_for_test_orders = random.choices(all_items, k=20)
        for _ in range(30):
            order = Order.objects.create(project=random.choice(all_projects), created_by=test_user)
            OrderStateToOrder.objects.create(
                order=order,
                state=order_states['Активный'],
                finished_date=datetime.datetime.now()
            )
            OrderStateToOrder.objects.create(
                order=order,
                state=order_states['Завершен'],
            )
            for item in random.choices(items_for_test_orders, k=random.randint(1, 20)):
                qty = random.randint(1, 50)
                item_to_order = ItemToOrder.objects.get_or_create(
                    item=item,
                    order=order,
                    stage=random.choice(all_stages),
                    quantity=qty,
                    price_offer=PriceOffer.objects.create(
                        item=item,
                        for_quantity=qty,
                        price_per_unit=random.randint(100, 999)/100.00
                    )
                )[0]
                dt = random_date(datetime.datetime.strptime('5/25/2021 1:30 PM', '%m/%d/%Y %I:%M %p'), datetime.datetime.now())
                item_to_order.created_date = dt
                item_to_order.save()

        test_user.active_order = order
        test_user.save()
