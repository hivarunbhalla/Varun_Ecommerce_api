from django.db import transaction
from rest_framework import serializers
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, Review


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
        
        
class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only= True)
    
    class Meta:
        model = Customer
        fields = [ 'id', 'user_id', 'phone', 'birth_date', 'membership',]
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']
        
        
class OrderSerializer(serializers.ModelSerializer):
    
    items = OrderItemSerializer(many = True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items'] 
  
  
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
      

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk = cart_id).exists():
            raise serializers.ValidationError('No cart with given id found!')
        if CartItem.objects.filter(cart_id = cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']
            
            (customer, created) = Customer.objects.get_or_create(user_id = user_id)
            order = Order.objects.create(customer = customer)  # created an entry in database for order object
            
            
            # queryset for cart_items 
            cart_items = CartItem.objects \
                .select_related('product') \
                    .filter(cart_id = cart_id)
                    
            order_items = [
                OrderItem( 
                        order = order, 
                        product = item.product,
                        quantity = item.quantity,
                        unit_price = item.product.unit_price,
                ) for item in cart_items
            ]
            # Adding cart items to order items
            OrderItem.objects.bulk_create(order_items)
            
            Cart.objects.filter(pk = cart_id).delete()
            
            return order