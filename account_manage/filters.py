import django_filters
from .models import *
from django import forms
class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = order
        fields = '__all__'
        exclude = ['customer', 'date_ordered', 'amount']


class OrderListFilter(django_filters.FilterSet):
    class Meta:
        model = order
        fields = '__all__'
        exclude = ['date_ordered', 'amount']

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['product','category','status']
        exclude = ['date_created', 'price', 'stocks']

class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['date_created', 'email', 'telp']
        
