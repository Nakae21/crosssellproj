import csv
from django.core.management.base import BaseCommand
from core.models import Department, Aisle, Product, Order, OrderProduct
from django.db import transaction
from pathlib import Path

DATA_DIR = Path("dataset")  # Folder containing all CSV files

class Command(BaseCommand):
    help = "Import Instacart CSV files into the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting import...")

        with transaction.atomic():
            self.import_departments()
            self.import_aisles()
            self.import_products()
            self.import_orders()
            self.import_order_products()

        self.stdout.write(self.style.SUCCESS("✅ All data imported successfully."))

    def import_departments(self):
        with open(DATA_DIR / "departments.csv", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Department.objects.update_or_create(
                    department_id=row["department_id"],
                    defaults={"name": row["department"]}
                )
        self.stdout.write("✔️ Imported departments.")

    def import_aisles(self):
        with open(DATA_DIR / "aisles.csv", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Aisle.objects.update_or_create(
                    aisle_id=row["aisle_id"],
                    defaults={"name": row["aisle"]}
                )
        self.stdout.write("✔️ Imported aisles.")

    def import_products(self):
        with open(DATA_DIR / "products.csv", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                aisle = Aisle.objects.get(aisle_id=row["aisle_id"])
                department = Department.objects.get(department_id=row["department_id"])
                Product.objects.update_or_create(
                    product_id=row["product_id"],
                    defaults={
                        "name": row["product_name"],
                        "aisle": aisle,
                        "department": department
                    }
                )
        self.stdout.write("✔️ Imported products.")

    def import_orders(self):
        with open(DATA_DIR / "orders.csv", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                Order.objects.update_or_create(
                    order_id=row["order_id"],
                    defaults={
                        "user_id": row["user_id"],
                        "order_number": row["order_number"],
                        "order_dow": row["order_dow"],
                        "order_hour_of_day": row["order_hour_of_day"],
                        "days_since_prior_order": row["days_since_prior_order"] or None
                    }
                )
        self.stdout.write("✔️ Imported orders.")

    def import_order_products(self):
        files = ["order_products__train.csv", "order_products__prior.csv"]
        for file_name in files:
            with open(DATA_DIR / file_name, newline='', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    order = Order.objects.get(order_id=row["order_id"])
                    product = Product.objects.get(product_id=row["product_id"])
                    OrderProduct.objects.update_or_create(
                        order=order,
                        product=product,
                        defaults={
                            "add_to_cart_order": row["add_to_cart_order"],
                            "reordered": row["reordered"] == "1"
                        }
                    )
        self.stdout.write("✔️ Imported order-product relationships.")
