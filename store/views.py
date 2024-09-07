from django.shortcuts import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response

from core import serializers
from store.permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermission
from .models import Cart, CartItem, Collection, Customer, Order, Product, OrderItem, ProductImage, Review
from .filters import ProductFilter, ReviewFilter
from .pagination import DefaultPagination
from .serializers import AddCartItemSerializer, CartSerializer, CartItemSerializer, CollectionSerializer, CreateOrderSerializer, CustomerSerializer, OrderItemSerializer, OrderSerializer, ProductImageSerializer, ProductSerializer, UpdateCartItemSerializer, ReviewSerializer, UpdateOrderSerializer



def home(request):
    return HttpResponse("Welcome to Store Homepage")

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description',]
    ordering_fields = ['title', 'unit_price', 'inventory', 'last_update']
    
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    
    # Filters logic without django-filter
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     # query_params is a dictionary
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id = collection_id)
    #     return queryset
    
    def get_serializer_context(self):
        return {
            'request': self.request
        }
        
    def destroy(self, request, *args, **kwargs):
    
        # Check if there are any associated order items
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Product cannot be deleted as it is associated with some order items'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().destroy(request, *args, **kwargs)
        
'''       
@api_view(['GET', 'POST', ])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many = True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    elif request.method == 'DELETE':
        if product.orderitems.count()>0:
            return Response({ 'error' : 'This Product cannot be deleted as it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'featured_product__title']
    ordering_fields = ['title', ]
    
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    
    
    def get_serializer_context(self):
        return {
            'request' : self.request
        }    
        
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id = kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Collection cannot be deleted as it is associated with some products'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(self, request, *args, **kwargs)
    
'''
@api_view(['GET', 'POST', ])
def collection_list(request):
    if request.method == 'GET':   
        queryset = Collection.objects.select_related('featured_product').all()
        serializer = ProductSerializer(queryset, many = True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data) 
'''


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReviewFilter
    search_fields = ['title', 'description']
    ordering_fields = ['rating', ]
    
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
    def get_serializer_context(self):
        return {
            'product_id' : self.kwargs['product_pk']
        }
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])
    
    
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('cart_items__product').all()
    serializer_class = CartSerializer
    
    
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', ]
    
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
          
    
    def get_serializer_context(self):
        return {
            'cart_id' : self.kwargs.get('cart_pk')
        }
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id = self.kwargs['cart_pk'])
        
            
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    permission_classes = [FullDjangoModelPermissions]
    
    @action(detail=True, permission_classes = [ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes = [IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        if not user_id:
            return Response({'error': 'User ID is required (Add Access Token)'}, status=status.HTTP_400_BAD_REQUEST)
    
        customer = Customer.objects.get(user_id=user_id)
        
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data)
        
        
class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data = request.data, 
            context = {
                'user_id': self.request.user.id,
            }
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # new serializer used to deserialise created order so that it can be retured to client
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        
        customer_id = Customer.objects.only('id').get(user_id = user.id)
        return Order.objects.filter(customer_id = customer_id)
    
        
class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        return {
            'order_id' : self.kwargs.get('order_pk')
        }
    
    def get_queryset(self):
        return OrderItem.objects.filter(order_id = self.kwargs['order_pk'])


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    
    def get_queryset(self):
        return ProductImage.objects.filter(product_id = self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {
            'product_pk' : self.kwargs['product_pk']
        }
    
    
    