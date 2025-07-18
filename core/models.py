from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity


# Department model from departments.csv
class Department(models.Model):
    department_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Aisle model from aisles.csv
class Aisle(models.Model):
    aisle_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Product model from products.csv
class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=255)
    aisle_id = models.IntegerField()
    department_id = models.IntegerField()

    def __str__(self):
        return self.product_name

# Order model from orders.csv
class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    order_number = models.IntegerField(default=1)
    order_dow = models.IntegerField(default=0)
    order_hour_of_day = models.IntegerField(default=12)
    days_since_prior_order = models.FloatField(default=0.0)

    def __str__(self):
        return f"Order {self.order_id} (User {self.user_id})"


# OrderProduct model from order_products__train.csv and order_products__prior.csv
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    add_to_cart_order = models.IntegerField()
    reordered = models.BooleanField()

    def __str__(self):
        return f"{self.product.name} in Order {self.order.order_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    add_to_cart_order = models.IntegerField()
    reordered = models.BooleanField()

    def __str__(self):
        return f"OrderItem: Order {self.order.order_id}, Product {self.product.product}"