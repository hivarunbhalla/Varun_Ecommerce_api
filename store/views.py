
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Collection, Product, OrderItem, Review
from .filters import ProductFilter, ReviewFilter
from .pagination import DefaultPagination
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer



def home(request):
    return HttpResponse("Welcome to Store Homepage")

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description',]
    ordering_fields = ['title', 'unit_price', 'inventory', 'last_update']
    
    pagination_class = DefaultPagination
    
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
    
    def get_serializer_context(self):
        return {
            'product_id' : self.kwargs['product_pk']
        }
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])