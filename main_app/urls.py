from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('inventory/', views.inventory_index, name='index'),
    path('inventory/<int:item_id>/', views.inventory_detail, name='detail'),
    path('inventory/create/', views.ItemCreate.as_view(), name='inventory_create'),
    path('inventory/<int:pk>/update/', views.ItemUpdate.as_view(), name='inventory_update'),
    path('inventory/<int:pk>/delete/', views.ItemDelete.as_view(), name='inventory_delete'),
]