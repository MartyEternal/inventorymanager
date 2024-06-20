from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    quantity_current = models.IntegerField()
    quantity_max = models.IntegerField()

    def __str__(self):
        return self.name