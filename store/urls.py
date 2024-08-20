from cgitb import lookup
from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename = 'products')
router.register('collections', views.CollectionViewSet, basename = 'collections')

#NESTED ROUTERS
products_router = routers.NestedDefaultRouter(router, 'products', lookup= 'product')
products_router.register('reviews', views.ReviewViewSet, basename = 'product-reviews')



urlpatterns = (
                router.urls
                + products_router.urls
                
            )


# URLConf
# urlpatterns = [
#     path('', views.home, name='home'),
#     path('products/', views.product_list, name='product_list'),
#     path('products/<int:pk>/', views.product_detail, name='product_detail'),
#     # path('collections/', views.collection_list, name='collection_list'),
#     path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),
# ]
