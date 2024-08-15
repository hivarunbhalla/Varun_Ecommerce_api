from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    # path('collections/', views.collection_list, name='collection_list'),
    path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),
]
