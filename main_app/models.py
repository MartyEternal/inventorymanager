from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

#category stuff
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('categories_detail', kwargs={'category_id': self.id})
    
    # Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity_current = models.IntegerField()
    quantity_min = models.IntegerField(default = 1)
    quantity_max = models.IntegerField()
    description = models.TextField(max_length=250)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'item_id': self.id})