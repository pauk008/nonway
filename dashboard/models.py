from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Non nomi")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Narxi (so'm)")
    image = models.ImageField(upload_to='products/', verbose_name="Rasmi")
    is_available = models.BooleanField(default=True, verbose_name="Sotuvda bormi")

    def __str__(self):
        return self.name