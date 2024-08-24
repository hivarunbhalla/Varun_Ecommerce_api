from dataclasses import field
from rest_framework import serializers
from .models import Cart, CartItem, Product, Collection, Review

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
        fields = ['id', 'title', 'sku', 'unit_price']
        
    
class ReviewSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only = True) 
    id = serializers.IntegerField(read_only = True)
    class Meta:
        model = Review
        fields = ['id', 'date', 'product', 'rating','title', 'description']
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(
            product_id = product_id,
            **validated_data
        )
        
        
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only = True)
    total_price = serializers.SerializerMethodField()


    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
        
    def get_total_price(self, obj):
        return obj.quantity * obj.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only = True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart    
        fields = ['id', 'cart_items', 'total_price'] #get cart items using FK related name
        read_only_fields = ['id', 'total_price']  # reasearch why cart_items are unable to make as readonly using this method
        
    def get_total_price(self, cart):
        all_products_total_price = [ item.quantity * item.product.unit_price \
                            for item in cart.cart_items.all()] 
        return sum(all_products_total_price)
    
    
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    def validate_product_id(self, pid):
        if not Product.objects.filter(pk=pid).exists():
            raise serializers.ValidationError('No product found with given product id')
        return pid
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        try:
            #updating qty
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id = product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            #create new item
            cart_item = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            self.instance = cart_item # read docs about Models Serializer and its base save method
            
        return self.instance
            
            
    
    class Meta:
        model = CartItem
        fields = [ 'id', 'product_id', 'quantity']
        
        
class UpdateCartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['quantity']