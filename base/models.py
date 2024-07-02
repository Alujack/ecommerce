from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True, null=False)
    password_hash = models.CharField(max_length=255, null=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='images/users', null=True, blank=True)

class Stock(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Store(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    address = models.ForeignKey("Address", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CustomerList(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Address(models.Model):
    users = models.ManyToManyField(User)
    unit_number = models.IntegerField(null=True, blank=True)
    street_number = models.IntegerField(null=True, blank=True)
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)


class ProductCategory(models.Model):
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    category_name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='images/categories/', null=True, blank=True)


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    product_image = models.ImageField(
        upload_to='images/product/', null=True, blank=True)
    price = models.PositiveIntegerField()


class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_in_stock = models.PositiveIntegerField()
    variations = models.ManyToManyField(
        'VariationOption', through='ProductConfiguration')


class Variation(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    attribute_type = models.CharField(max_length=255, null=True, blank=True)


class VariationOption(models.Model):
    variation = models.ForeignKey(
        Variation, on_delete=models.CASCADE, null=True, blank=True)
    option_value = models.CharField(max_length=255, null=True, blank=True)


class ProductConfiguration(models.Model):
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    variation_option = models.ForeignKey(
        VariationOption, on_delete=models.CASCADE, null=True, blank=True)


class Promotion(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    discount_percentage = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    categories = models.ManyToManyField(
        ProductCategory, through='PromotionCategory', null=True, blank=True)


class PromotionCategory(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)


class OrderLine(models.Model):
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    order = models.ForeignKey('ShopOrder', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()


class ShoppingCartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()


class PaymentType(models.Model):
    type_value = models.CharField(max_length=255)
    # e.g., MasterCard, Visa, ABA, QR


class UserPaymentMethod(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    payment_type = models.ForeignKey(
        PaymentType, on_delete=models.CASCADE)
    provider = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    expiry_date = models.DateField()


class UserReview(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    order_product = models.ForeignKey(
        OrderLine, on_delete=models.CASCADE, null=True, blank=True)
    review_text = models.TextField()
    rating = models.PositiveIntegerField()


class ShopOrder(models.Model):
    STATUS = [
        ('pending', 'pending'),
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('delivered', 'delivered')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, blank=True)
    order_date = models.DateField(auto_now_add=True)
    payment_method = models.ForeignKey(
        UserPaymentMethod, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255)
    shipping_method = models.ForeignKey(
        'ShippingMethod', on_delete=models.CASCADE, null=True, blank=True)
    order_total = models.PositiveIntegerField()
    status = models.CharField(max_length=255, choices=STATUS, null=True, blank=True)


class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderLine, on_delete=models.CASCADE)


class ShippingMethod(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Draft(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)


class Publish(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
