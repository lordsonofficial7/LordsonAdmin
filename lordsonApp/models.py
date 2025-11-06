from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')
    description = models.TextField(blank=True, null=True)  # ✅ optional field
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('tshirt', 'T-Shirt'),
        ('sweatshirt', 'Sweatshirt'),
    ]

    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', '2X Large'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    # ⬇️ Store multiple sizes as comma-separated values
    sizes = models.JSONField(default=list, blank=True)
    image = models.ImageField(upload_to='products/')
    final_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.discount:
            self.final_price = self.price - (self.price * self.discount / 100)
        else:
            self.final_price = self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Image for {self.product.title}"





class Order(models.Model):
    PAYMENT_METHODS = [
        ("COD", "Cash on Delivery"),
        # ("ONLINE", "Online Payment"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("VERIFIED", "Verified"),
        ("REJECTED", "Rejected"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
    ]

    customer_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default="COD")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    cart_data = models.JSONField()  # store cart info directly from frontend
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} ({self.status})"