from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Item, Category, HistoryLog, QuantityLog
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, QuantityChangeForm
from django.utils.decorators import method_decorator

# main stuff
def about(request):
    return render(request, 'about.html')

def pricing(request):
    return render(request, 'pricing.html')

def contact(request):
    return render(request, 'contact.html')

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
    fields = ['name', 'description']

class CategoryUpdate(UpdateView):
    model = Category
    fields = ['name', 'description']
    success_url = '/categories'

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
  fields = ['name', 'description', 'quantity_min','quantity_max']

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

def search(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            searched = request.POST['searched']
            items = Item.objects.filter(name__icontains=searched)
            categories = Category.objects.filter(name__icontains=searched)
            return render(request, 'search.html', {'searched':searched, 'item': items, 'category': categories})
        else:
            return render (request, 'search.html', {})
    else:
        messages.success(request, 'You need to be logged in to search')
        return render('home')
    
def items_details(request, item_id):
    # item = Item.objects.get(id=item_id)
    item = get_object_or_404(Item, id=item_id)
    id_list = item.categories.all().values_list('id')
    categories_item_doesnt_have = Category.objects.exclude(id__in=id_list)
    last_quantity_changes = QuantityLog.objects.filter(item=item).order_by('-date_log')[:5]

    # for log in last_quantity_changes:
    #     previous_logs = QuantityLog.objects.filter(item=item, date_log__lt=log.date_log).order_by('-date_log')
    #     log.previous_count = previous_logs[0].change if previous_logs.exists() else item.quantity_current - log.change

    if request.method == 'POST':
        form = QuantityChangeForm(request.POST)
        if form.is_valid():
            quantity_log = form.save(commit=False)
            quantity_log.item = item
            quantity_log.user = request.user
            quantity_log.previous_count = item.quantity_current
            item.quantity_current = quantity_log.change
            item.save()
            quantity_log.save()
            return redirect('detail', item_id=item_id)
    
    else:
        form = QuantityChangeForm()

    for log in last_quantity_changes:
        previous_logs = QuantityLog.objects.filter(item=item, date_log__lt=log.date_log).order_by('-date_log')
        log.previous_count = previous_logs[0].change if previous_logs.exists() else item.quantity_current - log.change

    return render(request, 'items/detail.html', {
        'item':item, 
        'categories':categories_item_doesnt_have, 
        'last_quantity_changes': last_quantity_changes, 
        'form': form,
    })

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
    history = HistoryLog.objects.all().order_by('-date_log')
    quantity_logs = QuantityLog.objects.all().order_by('-date_log')
    return render(request, 'main_app/history_log.html', {'history': history, 'logs': quantity_logs,})

def change_quantity(request):
    if request.method == "POST":
        form = QuantityChangeForm(request.POST)
        if form.is_valid():
            quantity_log = form.save(commit=False)
            item = quantity_log.item
            item.quantity_current =+ quantity_log.change
            item.save()
            quantity_log.user = request.user
            quantity_log.save()
            return redirect('quantity_log')
    else:
        form = QuantityChangeForm()
    return render(request, 'main_app/change_quantity.html', { 'form': form })

def quantity_log(request):
    logs = QuantityLog.objects.all().order_by('-date_log')
    return render(request, 'main_app/quantity_log.html', { 'logs': logs })