from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('pricing/', views.pricing, name='pricing'),
    path('contact/', views.contact, name='contact'),

    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    # categories stuff
    path('categories/', views.categories_index, name='categories_index'),
    path('categories/<int:category_id>/', views.categories_detail, name='categories_detail'),
    path('categories/create/', views.CategoryCreate.as_view(), name='categories_create'),
    path('categories/<int:pk>/update/', views.CategoryUpdate.as_view(), name='categories_update'),
    path('categories/<int:pk>/delete/', views.CategoryDelete.as_view(), name='categories_delete'),

    
    # items stuff
    path('items/<int:item_id>/', views.items_details, name='detail'),  
    path('items/create/', views.ItemCreate.as_view(), name='items_create'),  
    path('items/<int:pk>/update/', views.ItemUpdate.as_view(), name='items_update'),
    path('items/<int:pk>/delete/', views.ItemDelete.as_view(), name='items_delete'),  
    path('items/<int:item_id>/assoc_category/<int:category_id>/', views.assoc_category, name='assoc_category'),
    path('items/<int:item_id>/unassoc_category/<int:category_id>/', views.unassoc_category, name='unassoc_category'),
    
    # search bar
    path('search/', views.search, name='search'),

    # history log
    path('history_log/', views.history_log, name='history_log'),
    path('change_quantity/', views.change_quantity, name='change_quantity'),
    path('quantity_log/', views.quantity_log, name='quantity_log'),
]