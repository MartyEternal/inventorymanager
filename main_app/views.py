from django.shortcuts import render

inventory = [
    {'name': 'Table Fork', 'type': 'utensil', 'description': 'This is a table fork. It is designed for the main dish.', 'quantity_current': 4, 'quantity_max': 50},
    {'name': 'Table Spoon', 'type': 'utensil', 'description': 'This is a table spoon. The large spoon is used for serving.', 'quantity_current': 3, 'quantity_max': 50},
]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def inventory_index(request):
    return render(request, 'inventory/index.html', {
        'inventory': inventory
    })