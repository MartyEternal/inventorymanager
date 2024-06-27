from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Item, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required




def about(request):
    return render(request, 'about.html')





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

# categories stuff
def categories_index(request):
    categories = Category.objects.all()
    return render(request, 'categories/index.html', {
        'categories': categories
    })

def categories_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    return render(request, 'categories/detail.html', { 'category': category })

class CategoryCreate(CreateView):
    model = Category
    fields = '__all__'

class CategoryUpdate(UpdateView):
    model = Category
    fields = '__all__'

class CategoryDelete(DeleteView):
    model = Category
    success_url = '/categories'

class ItemUpdate(UpdateView):
  model = Item
  fields = ['type', 'description', 'quantity_current','quantity_max']

class ItemDelete(DeleteView):
  model = Item
  success_url = '/'

