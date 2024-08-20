from dataclasses import field
from django_filters import rest_framework as filters
from django_filters.rest_framework import FilterSet
from .models import Product, Review

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id' : ['exact'],
            'unit_price' : ['gte', 'lte'],
            
        }
        
class ReviewFilter(FilterSet):
    min_rating = filters.NumberFilter(field_name='rating', lookup_expr='gte')  # For "greater than or equal to"
    max_rating = filters.NumberFilter(field_name='rating', lookup_expr='lte')  # For "less than or equal to"

    class Meta:
        model = Review
        fields = ['min_rating', 'max_rating']
        