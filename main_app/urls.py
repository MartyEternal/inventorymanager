from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_user, name='logout'),
    # categories stuff
    path('categories/', views.categories_index, name='categories_index'),
    path('categories/<int:category_id>/', views.categories_detail, name='categories_detail'),
    path('categories/create/', views.CategoryCreate.as_view(), name='categories_create'),
    path('categories/<int:pk>/update/', views.CategoryUpdate.as_view(), name='categories_update'),
    path('categories/<int:pk>/delete/', views.CategoryDelete.as_view(), name='categories_delete'),
    path('item/', views.item_index, name='item'),
    path('item/<int:item_id>/', views.item_detail, name='detail'),
    path('item/create/', views.ItemCreate, name='item_create'),
    path('item/<int:pk>/update/', views.ItemUpdate.as_view(), name='item_update'),
    path('item/<int:pk>/delete/', views.ItemDelete.as_view(), name='item_delete'),  
]