from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название компании")
    tax_id = models.CharField(max_length=20, unique=True, verbose_name="ИНН")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ContactPerson(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name
