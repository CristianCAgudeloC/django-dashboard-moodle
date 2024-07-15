from django.urls import path
from . import views
from .views import ItemListCreate, ItemDetail

urlpatterns = [
    path('', views.home, name='home'),
    path('api/items/', ItemListCreate.as_view(), name='item-list-create'),
    path('api/items/<int:pk>/', ItemDetail.as_view(), name='item-detail'),
]