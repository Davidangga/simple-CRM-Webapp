from django import forms
from .models import Product,order,ProductGroup,Product,Customer
from django.forms.models import inlineformset_factory, modelformset_factory
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#create user registration

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CustomerCreate(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['date_created']
        widgets = {
            'username' : forms.TextInput(attrs={'placeholder':'Username','class':'border'}),
            'email' : forms.TextInput(attrs={'placeholder':'Email','class':'border'}),
            'telp' : forms.TextInput(attrs={'placeholder':'Phone','class':'border'}),
        }

class ProductUpdate(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['date_created']
        widgets = {
            'category': forms.Select(attrs={'class':'border'}),
            'product' : forms.TextInput(attrs={'placeholder':'Username','class':'border'}),
            'status': forms.Select(attrs={'class':'border'}),
            'stocks' : forms.NumberInput(attrs={'class':'border'}),
            'price' : forms.NumberInput(attrs={'class':'border'}),
        }

# Create Inline orders
class PlaceOrderForm(forms.ModelForm):
    class Meta:
        model = order
        exclude = ['date_ordered','customer']

OrderInlineFormset = inlineformset_factory(Customer,order,form = PlaceOrderForm,extra=1,can_delete=True)


class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = order
        exclude = ['date_ordered','customer']
        widgets = {
            'product': forms.Select(attrs={'class':'border-select'}),
            'payment_status': forms.Select(attrs={'class':'border-select'}),
            'status' : forms.Select(attrs={'class':'border-select'}),
            'amount' : forms.NumberInput(attrs={'class':'border-select'}),
        }


# Create Inline products
class PlaceProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        
        fields = ['category','product','stocks','status','price']

ProductsFormset = inlineformset_factory(
    ProductGroup,Product,form = PlaceProductsForm,
    extra=1)
