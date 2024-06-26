from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('item/', views.item_index, name='item'),
    path('item/<int:item_id>/', views.item_detail, name='detail'),
    path('item/create/', views.ItemCreate, name='item_create'),
    path('item/<int:pk>/update/', views.ItemUpdate, name='item_update'),
    path('item/<int:pk>/delete/', views.ItemDelete, name='item_delete'),
    path('logout/', views.logout_user, name='logout'),
    
]