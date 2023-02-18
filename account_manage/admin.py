from django.contrib import admin
from .models import Customer,Product,Tag,order,ProductGroup
# Register your models here.
class ProductInlines(admin.TabularInline):
    model = Product
    extra = 1

class ProductGroupAdmin(admin.ModelAdmin):
    inlines = [
        ProductInlines,
    ]
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(ProductGroup,ProductGroupAdmin)

class OrdersInlines(admin.TabularInline):
    model = order
    extra = 1
class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [('name:',{'fields' : ['username']}),('Email:',{'fields' : ['email']}),('Telp.No:',{'fields' : ['telp']})]
    inlines = [
        OrdersInlines,
    ]

admin.site.register(Customer,CustomerAdmin)
