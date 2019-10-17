from django.shortcuts import render
from .serializers import itemSerializer 
from .models import item 

#from rest_framework import generics
#from rest_framework.filters import SearchFilter
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets 
import django_filters
from rest_framework import filters
from django_filters import rest_framework

class itemView(viewsets.ModelViewSet): 
    serializer_class = itemSerializer 
    queryset = item.objects.all()

    filter_backends = (filters.SearchFilter,)
    search_fields = ('category_level_2', 'item_name', 'item_brand')
    #filter_backends = (rest_framework.DjangoFilterBackend, )
    #filters.SearchFilter, filters.OrderingFilter, )
    #filter_class = itemFilter

''' work in filter type. 
class itemFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.CharFilter(field_name='item_name', lookup_expr='icontains')
    brand = django_filters.CharFilter(field_name='item_brand', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category_level_2',lookup_expr='icontains')
    
    class Meta:
        model = item
        fields = ['category_level_2','item_name', 'item_brand',]
'''    