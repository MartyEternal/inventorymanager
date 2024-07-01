from django.contrib import admin
from .models import Item, Category, HistoryLog, QuantityLog
# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(HistoryLog)
admin.site.register(QuantityLog)