from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify

class Promotion(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('PERCENTAGE', 'Percentage'),
        ('FIXED_AMOUNT', 'Fixed Amount'),
        ('BOGO', 'Buy One Get One'),
        ('FREE_SHIPPING', 'Free Shipping'),
    ]
    DEFAULT_DISCOUNT_TYPE = ('PERCENTAGE', 'Percentage')
    code = models.CharField(max_length=50)

    description = models.CharField(max_length=255)
    discount_type = models.CharField(
        max_length=20, 
        choices=DISCOUNT_TYPE_CHOICES, 
        default=DEFAULT_DISCOUNT_TYPE
        )
    discount_value = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.code} - {self.description[:10]}'


class Collection(models.Model):
    title  = models.CharField(max_length=250)
    description = models.TextField()
    featured_product = models.ForeignKey(
        "Product", 
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+'  #don't make reverse relation with Product Models
        )

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    sku = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal(1.0))])

    #don't delete product if collection got deleted
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products', null=True, blank=True)
    promotions = models.ManyToManyField("Promotion", blank=True)

    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_update = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:  # Only set the slug if it hasn't been set yet
            self.slug = slugify(self.title)  # Generate the slug from the title
        super().save(*args, **kwargs)  # Call the original save method


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name', 'last_name']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True, editable=False)
    payment_status = models.CharField(
        max_length=1, 
        choices=PAYMENT_STATUS_CHOICES, 
        default=PAYMENT_STATUS_PENDING
        )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    house_number = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return f'Review for {self.product.title}: {self.title}'
    
