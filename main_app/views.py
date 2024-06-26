from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Item
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# item = [
#     {'name': 'Table Fork', 'type': 'utensil', 'description': 'This is a table fork. It is designed for the main dish.', 'quantity_current': 4, 'quantity_max': 50},
#     {'name': 'Table Spoon', 'type': 'utensil', 'description': 'This is a table spoon. The large spoon is used for serving.', 'quantity_current': 3, 'quantity_max': 50},
# ]

# Create your views here.
@login_required
class ItemCreate(CreateView):
    model = Item
    fields = '__all__'

@login_required
class ItemUpdate(UpdateView):
  model = Item
  fields = ['type', 'description', 'quantity_current', 'quantity_max']

@login_required
class ItemDelete(DeleteView):
  model = Item
  success_url = '/item'

# def home(request):
#     return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def item_index(request):
    item = Item.objects.all()
    return render(request, 'item/index.html', {
        'item': item
    })

@login_required
def item_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'item/detail.html', { 'item': item })

def home(request):
    items = Item.objects.all()
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in, welcome!')
            return redirect('home')
        else:
            messages.success(request, 'There was an error logging in, please try again.')
            return redirect('home')
    else:
        return render(request, 'home.html', {'items': items})
    
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')