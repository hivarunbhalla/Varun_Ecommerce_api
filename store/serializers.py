from rest_framework import serializers
from .models import Product, Collection, Review

class CollectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    
    
    class Meta:
        model = Collection
        fields = ['id', 'title', 'description', 'featured_product']
    
    def create(self, validated_data):
        return super().create(validated_data)
    


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'collection']

    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=models.Collection.objects.all(),
    #     view_name='collection-detail',
    # )
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'sku']
        
    
class ReviewSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only = True) 
    id = serializers.IntegerField(read_only = True)
    class Meta:
        model = Review
        fields = ['id', 'date', 'product', 'title', 'description']
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(
            product_id = product_id,
            **validated_data
        )