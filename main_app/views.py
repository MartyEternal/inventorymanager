from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Item

# inventory = [
#     {'name': 'Table Fork', 'type': 'utensil', 'description': 'This is a table fork. It is designed for the main dish.', 'quantity_current': 4, 'quantity_max': 50},
#     {'name': 'Table Spoon', 'type': 'utensil', 'description': 'This is a table spoon. The large spoon is used for serving.', 'quantity_current': 3, 'quantity_max': 50},
# ]

# Create your views here.
class ItemCreate(CreateView):
    model = Item
    fields = '__all__'

class ItemUpdate(UpdateView):
  model = Item
  fields = ['type', 'description', 'quantity_current', 'quantity_max']

class ItemDelete(DeleteView):
  model = Item
  success_url = '/inventory'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def inventory_index(request):
    inventory = Item.objects.all()
    return render(request, 'inventory/index.html', {
        'inventory': inventory
    })

def inventory_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'inventory/detail.html', { 'item': item })
