from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Item, Category, HistoryLog
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

# main stuff
def about(request):
    return render(request, 'about.html')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm((request.POST))
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You are registered, Welcome!')
            return redirect('home')
    else:
        form = SignUpForm()    
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})

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

# item stuff    
class ItemCreate(CreateView):
    model = Item
    fields = ['name', 'description', 'quantity_current','quantity_max']
    success_url = '/'

    def form_valid(self, form):
        response = super().form_valid(form)
        category = self.object.categories.first() if self.object.categories.exists() else None
        HistoryLog.objects.create(
            item=self.object,
            category=category,
            user=self.request.user,
            description=f"[Item] '{self.object.name}' was added.",
            quantity=self.object.quantity_current
        )
        return response

class ItemUpdate(UpdateView):
  model = Item
  fields = ['name', 'description', 'quantity_current', 'quantity_min','quantity_max']

  def form_valid(self, form):
        response = super().form_valid(form)
        category = self.object.categories.first() if self.object.categories.exists() else None
        HistoryLog.objects.create(
            item=self.object,
            category=category,
            user=self.request.user,
            description=f"[Item] '{self.object.name}' was updated.",
            quantity=self.object.quantity_current
        )
        return response

class ItemDelete(DeleteView):
  model = Item
  success_url = '/'

  def delete(self, request, *args, **kwargs):
      item = self.get_object()
      # category = item.categories.first() if item.categories.exists() else None
      HistoryLog.objects.create(
          item=item,
          user=request.user,
          description=f"[Item] '{item.name}' was deleted.",
          quantity=item.quantity_current
      )
      response = super().delete(request, *args, **kwargs)
      return response

def search_items(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            searched = request.POST['searched']
            items = Item.objects.filter(name__icontains=searched)
            print(items)
            print(searched)
            return render(request, 'search_items.html', {'searched':searched, 'item': items})
        else:
            return render (request, 'search_items.html', {})
    else:
        messages.success(request, 'You need to be logged in to search')
        return render('home')
    
def items_details(request, item_id):
    item = Item.objects.get(id=item_id)
    id_list = item.categories.all().values_list('id')
    categories_item_doesnt_have = Category.objects.exclude(id__in=id_list)
    return render(request, 'items/detail.html', {'item':item, 'categories':categories_item_doesnt_have})

# association stuff
def assoc_category(request, item_id, category_id):
    item = get_object_or_404(Item, id=item_id)
    category = get_object_or_404(Category, id=category_id)
    item.categories.add(category)
    # Item.objects.get(id=item_id).categories.add(category_id)
    HistoryLog.objects.create(
        item=item,
        category=category,
        user=request.user,
        description=f"'{item.name}' has been filed under '{category.name}'.",
        quantity=item.quantity_current
    )
    return redirect('detail',item_id=item_id)

def unassoc_category(request, item_id, category_id):
    item = get_object_or_404(Item, id=item_id)
    category = get_object_or_404(Category, id=category_id)
    item.categories.remove(category)
    # Item.objects.get(id=item_id).categories.add(category_id)
    HistoryLog.objects.create(
        item=item,
        category=category,
        user=request.user,
        description=f"'{item.name}' has been removed from '{category.name}'.",
        quantity=item.quantity_current
    )
    return redirect('detail',item_id=item_id)

# history log stuff
def history_log(request):
    history = HistoryLog.objects.all()
    return render(request, 'main_app/history_log.html', {'history': history})