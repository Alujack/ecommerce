from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='images/users', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'phone_number', 'role', 'image']

    def __str__(self):
        return self.email

class Store(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    address = models.ForeignKey(
        "Address", on_delete=models.CASCADE, null=True, blank=True)


class CustomerList(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Address(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    house_number = models.CharField(max_length=255, null=True, blank=True)
    street_number = models.CharField(max_length=255, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    commune = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    
class ProductCategory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    category_name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='images/categories/', null=True, blank=True)

class Variations(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    attribute_type = models.CharField(max_length=255, null=True, blank=True)

  


class VariationOption(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    variation = models.ForeignKey(
        Variations,  related_name='options',null=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, null=True, blank=True)




class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images/products/', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(
        Store, related_name='products', on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField(
        ProductCategory, related_name='products')



class ProductItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, related_name='variations',null=True, on_delete=models.CASCADE)
    variation_options = models.ManyToManyField(
        VariationOption, related_name='product_variations')



class Stock(models.Model):
    id = models.UUIDField(
         primary_key=True, default=uuid.uuid4, editable=False)
    quantity = models.IntegerField()
    variation = models.ForeignKey(ProductItem, related_name='stock', null=True, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, related_name='stock', on_delete=models.CASCADE, null = True)


    
class Promotion(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    discount_percentage = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    categories = models.ManyToManyField(
        ProductCategory, through='PromotionCategory')


class PromotionCategory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)


class OrderLine(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    order = models.ForeignKey('ShopOrder', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()


class ShoppingCartItem(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()


class PaymentType(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    type_value = models.CharField(max_length=255)
    # e.g., MasterCard, Visa, ABA, QR


class UserPaymentMethod(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    provider = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    expiry_date = models.DateField()


class UserReview(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    order_product = models.ForeignKey(
        OrderLine, on_delete=models.CASCADE, null=True, blank=True)
    review_text = models.TextField()
    rating = models.PositiveIntegerField()


class ShopOrder(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    STATUS = [
        ('pending', 'pending'),
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('delivered', 'delivered')
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateField(auto_now_add=True)
    payment_method = models.ForeignKey(
        UserPaymentMethod, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255)
    shipping_method = models.ForeignKey(
        'ShippingMethod', on_delete=models.CASCADE, null=True, blank=True)
    order_total = models.PositiveIntegerField()
    status = models.CharField(
        max_length=255, choices=STATUS, null=True, blank=True)


class OrderHistory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderLine, on_delete=models.CASCADE)


class ShippingMethod(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    name = models.CharField(max_length=255)
    price = models.FloatField()


class Favourite(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Draft(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)


class Publish(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
