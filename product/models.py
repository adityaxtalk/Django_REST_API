from django.db import models

class Product(models.Model):
    title =models.CharField(max_length=100,blank=False)
    description=models.CharField(max_length=200,blank=True)
    imageURL=models.URLField(max_length=300,blank=False)
    price=models.DecimalField(max_digits=10,decimal_places=2,blank=False)

    def __str__(self):
        return f'Product: {self.title}\nDescription:{self.description}'