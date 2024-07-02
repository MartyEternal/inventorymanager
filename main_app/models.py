from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

#category stuff
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('categories_detail', kwargs={'category_id': self.id})
    
    # Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity_current = models.IntegerField(default=0)
    quantity_min = models.IntegerField(default = 1)
    quantity_max = models.IntegerField()
    description = models.TextField(max_length=1000)
    categories = models.ManyToManyField(Category)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'item_id': self.id})
    
class QuantityLog(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date_log = models.DateTimeField(auto_now_add=True)
    previous_count = models.IntegerField()
    change = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.date_log} - {self.item.name} - {self.change}'
    
class HistoryLog(models.Model):
    date_log = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=300)
    quantity = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.date_log} - {self.item.name}'
    
