from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('product', views.ProductViewSet, basename = 'products')
router.register('collections', views.CollectionViewSet, basename = 'collections')
router.register('cart', views.CartViewSet, basename = 'cart')
router.register('customers', views.CustomerViewSet, basename = 'customers')
router.register('orders', views.OrderViewSet, basename = 'orders')

#NESTED ROUTERS
products_router = routers.NestedDefaultRouter(router, 'product', lookup= 'product')
products_router.register('reviews', views.ReviewViewSet, basename = 'product-reviews')
products_router.register('images', views.ProductImageViewSet, basename = 'product-images')

cart_router = routers.NestedDefaultRouter(router, 'cart', lookup= 'cart')
cart_router.register('items', views.CartItemViewSet, basename = 'cart-items')

orders_router = routers.NestedDefaultRouter(router, 'orders', lookup= 'order')
orders_router.register('items', views.OrderItemViewSet, basename = 'oders-items')

# customer_router

urlpatterns = (
                router.urls
                + products_router.urls
                + cart_router.urls
                + orders_router.urls
            )


# URLConf
# urlpatterns = [
#     path('', views.home, name='home'),
#     path('products/', views.product_list, name='product_list'),
#     path('products/<int:pk>/', views.product_detail, name='product_detail'),
#     # path('collections/', views.collection_list, name='collection_list'),
#     path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),
# ]
