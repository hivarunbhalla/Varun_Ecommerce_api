
from django.shortcuts import HttpResponse, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Collection, Product, OrderItem, Review
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer


def home(request):
    return HttpResponse("Welcome to Store Homepage")

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
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
    
    def get_serializer_context(self):
        return {
            'product_id' : self.kwargs['product_pk']
        }
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])