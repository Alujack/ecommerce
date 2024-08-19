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


class CustomerList(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Address(models.Model):
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


class Store(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    address = models.ForeignKey(
        "Address", on_delete=models.CASCADE, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to='stores/logos', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)


class Category(models.Model):
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    category_name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        upload_to='images/seller/categories/', null=True, blank=True)


class Variations(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    attribute_type = models.CharField(max_length=255, null=True, blank=True)


class VariationOption(models.Model):
    variation = models.ForeignKey(
        Variations, related_name='options', null=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, null=True, blank=True)


class Product(models.Model):
    product_id = models.CharField(
        max_length=6, null=True, blank=True)
    name = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(
        Store, related_name='products', on_delete=models.CASCADE, null=True)
    image = models.ImageField(
        upload_to="image/products/", null=True, blank=True)
    categories = models.ManyToManyField(
        Category, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True, null=False)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='images/products/side', null=True, blank=True)
    angle = models.CharField(max_length=255, null=True, blank=True)
    # Store precomputed image features
    features = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Extract features if image is new or updated
        if self.image and not self.features:
            from search_app.services.image_processing import extract_image_features
            self.features = extract_image_features(self.image.path)
        super().save(*args, **kwargs)


class Stock(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    variation_option = models.ForeignKey(
        VariationOption, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()


class TechnicalDetail(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='technical_details')
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.key}: {self.value} for {self.product.title}"


class ProductRecommendation(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='recommended_products')
    recommended_product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='recommended_by')

    def __str__(self):
        return f"Recommendation: {self.recommended_product.title} for {self.product.title}"


class Pricing(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='pricing_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Price: {self.price} {self.currency} for {self.product.title}"


class CustomerReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField()
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True, null=False)
    review_title = models.CharField(max_length=255, null=True, blank=True)
    helpful_votes = models.IntegerField(default=0)

    def __str__(self):
        return f"Review by {self.customer.name} for {self.product.title}"


class Draft(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, null=True, blank=True)
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, null=True, blank=True)


class Publish(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, null=True, blank=True)
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)


class Promotion(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    discount_percentage = models.PositiveIntegerField()
    start_date = models.DateField(auto_now_add=True, null=False)
    end_date = models.DateField()
    categories = models.ManyToManyField(
        Category, through='PromotionCategory')


class PromotionCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)


class ShoppingCartItem(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()


class PaymentType(models.Model):
    type_value = models.CharField(max_length=255)
    # e.g., MasterCard, Visa, ABA, QR


class PaymentMethod(models.Model):
    id = models.UUIDField(
        primary_key=True, default=generate_uuid, editable=False)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    provider = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    expiry_date = models.DateField()


class ShopOrder(models.Model):
    STATUS = [
        ('pending', 'pending'),
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('delivered', 'delivered')
    ]
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateField(auto_now_add=True)
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255)
    shipping_method = models.ForeignKey(
        'ShippingMethod', on_delete=models.CASCADE, null=True, blank=True)
    order_total = models.PositiveIntegerField()
    status = models.CharField(
        max_length=255, choices=STATUS, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)


class OrderLine(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey('ShopOrder', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=False)


class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderLine, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)


class ShippingMethod(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Publish, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)


class Question(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return f"Question by {self.customer.name} on {self.product.title}"


class Answer(models.Model):
    question = models.OneToOneField(
        Question, on_delete=models.CASCADE, related_name='answer')
    answer_text = models.TextField()
    # e.g., 'Seller', 'Customer'
    answered_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return f"Answer to {self.question}"
