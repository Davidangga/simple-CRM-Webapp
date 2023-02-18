from django.shortcuts import render ,redirect ,reverse
from django.views import View
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView
from .models import Customer,order,Product,ProductGroup,Tag
from django.db import transaction
from . import form
from django.contrib import messages
from .filters import OrderFilter,ProductFilter,CustomerFilter,OrderListFilter
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import unautheticated_user, allowed_users,Admin_only
from django import forms

# Create your views here.

# tips in making class based view only using inherit from generic views if there is no other addition operation other than update delete, detail or list

#---------------------------------------------------------------------------------
# User registration and login

# class UserRegistration(View):
#     template_name = 'account/user_register.html'
#     @method_decorator(unautheticated_user) #decorators is place before view_funct yang mau di akses 
#     # for class based view decorator harus gunain method decorator
#     def get(self,*args,**kwargs):
#         myform = form.UserRegistrationForm()
#         context = {
#             'form':myform,
#         }
#         return render(self.request,self.template_name,context)

#     def post(self,*args,**kwargs):
#         myform = form.UserRegistrationForm(self.request.POST)
#         if myform.is_valid():
#             myform.save() 
#             user = myform.cleaned_data.get('username')
#             messages.success(self.request,'User {user} added'.format(user=user)) #messages succes only provide mesage when a certain operation is success
#             return redirect('manage:user-login')
#         else:
#             pass

#         context = {
#             'form':myform,
#         }
#         return render(self.request,self.template_name,context)

# class UserLogin(View):
#     @method_decorator(unautheticated_user)
#     def get(self,*args,**kwargs):
#         return render(self.request,'account/user_login.html')

#     def post(self,*args,**kwargs):
#         username = self.request.POST.get('username')
#         password = self.request.POST.get('password') #take input from html with name 'password'
#         user = authenticate(self.request,username=username,password=password) #check from user models return True or False
#         if user is not None:
#             login(self.request,user) 
#             return redirect('manage:dashboard')
#         else:
#             messages.warning(self.request,'Username or Password is incorrect')
#             return render(self.request,'account/user_login.html')

# class UserLogout(View):
#     def get(self,*args,**kwargs):
#         logout(self.request)
#         return redirect('manage:user-login')


# class UserPage(View):
#     def get(self,*args,**kwargs):
#         return render(self.request,'account/user-page.html')




#---------------------------------------------------------------------------------
# Dashboard

 #how to call decorator in generic class views
class Dashboard(ListView):
    # untuk masalah static di usahakan untuk menaruh folder unik untuk menempatkan folder images dan css agar tidak tabrakan
    template_name = 'account/dashboard.html'
    model = Customer
    # get_context_data ada di parent class funsinya menambah kan context yang bisa di akses seperti di function based view
    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)

        context.update({
            'customer': Customer.objects.order_by('-date_created')[:5],
            'order': order.objects.order_by('-date_ordered')[:5],
            'all_orders':order.objects.all(),
            'delivered_orders': order.objects.filter(status='Delivered'),
            'pending_orders': order.objects.filter(status='Pending'),
            'products' : Product.objects.all(),
        })
        return context

#---------------------------------------------------------------------------------
#Customer's View

class customers(ListView):
    template_name = 'account/customers.html'
    model = Customer
    context_object_name = 'customers'
    myfilter = CustomerFilter
    def get_queryset(self):
        return Customer.objects.order_by('username')
        
    def get_context_data(self, **kwargs):
        customers = self.get_queryset()
        myfilter = self.myfilter(self.request.GET,queryset=customers)
        customers = myfilter.qs
        unpaid_orders = []
        paid_orders = []
        for customer in customers:
            unpaid_orders.append(customer.order_set.filter(payment_status = 'Incomplete').count())
            paid_orders.append(customer.order_set.filter(payment_status = 'Complete').count())
        my_lists = zip(customers ,paid_orders ,unpaid_orders)
        context = {
            'mylists' :my_lists,
            'myfilter':myfilter,
        }
        return context
class customer(DetailView):
    model = Customer
    myfilter = OrderFilter
    template_name = 'account/customer.html'
    # it can be access in the temple using name object or model_name as a general name
    def get_context_data(self, **kwargs):
        context = super(customer, self).get_context_data(**kwargs)
        customer_access = Customer.objects.get(pk=self.kwargs.get('pk'))
        orders = customer_access.order_set.order_by('-date_ordered')
        myfilter = self.myfilter(self.request.GET,queryset=orders)
        orders  = myfilter.qs
        total_prices = []
        for order in orders:
            product_price = int(order.product.price)
            order_amount = int(order.amount)
            total = product_price * order_amount
            total_prices.append(total)
        context.update({
            'orders':zip(orders,total_prices),
            'myfilter':myfilter,
            'total_orders':orders.count,
        })
        return context

class Create_Customer(CreateView):
    form_class = form.CustomerCreate
    template_name = 'account/create-customer.html'
    def get_success_url(self):
        return reverse('manage:customers')

     # success url tidak bisa gunain redirect or reverse karena success url ini di jalankan pada ssat module di jalankan (parent class)
    #  sedangkan redirect dan reverse harus di jalankan ketika view run sehingga mereka dapat menemukan url yang sudah di buat.
class Update_Customer(UpdateView):
    form_class = form.CustomerCreate
    model = Customer
    template_name = 'account/update-customer.html'
    def get_success_url(self,*args,**kwargs):
        return reverse('manage:customer', kwargs={'pk': self.kwargs.get('pk')})

class Delete_Customer(View):
    def get(self,*args,**kwargs):
        deleted_customer = Customer.objects.get(pk=self.kwargs.get('pk'))
        deleted_customer.delete()
        return redirect('manage:customers')

    
#---------------------------------------------------------------------------------
# Product's View


class products(View):
    template_name = 'account/products.html'
    myfilter = ProductFilter

    def check_stock(self,product_name):
        product_checked = Product.objects.get(product=product_name)
        return product_checked.stocks
    def product_reduce(self,product_name,order_amount):
        updated_product = Product.objects.get(product=product_name)
        updated_product.stocks = updated_product.stocks - int(order_amount)
        updated_product.save()
    def add_stock_back(self,product_name,order_amount):
        updated_product = Product.objects.get(product=product_name)
        updated_product.stocks = updated_product.stocks + int(order_amount)
        updated_product.save()
    # @method_decorator(login_required())
    def get(self,request,*args,**kwargs):
        products = Product.objects.all()
        myfilter = self.myfilter(self.request.GET,queryset=products)
        products = myfilter.qs
        context = {
            'products' : products,
            'myfilter':myfilter,
        }
        return render(request,self.template_name,context)

class CreateProducts(CreateView):
    model = ProductGroup
    template_name = 'account/create-product.html'
    fields = ['category','tag']
    succeful_url = None

    def get_form(self, form_class = None):
        form = super(CreateProducts, self).get_form(form_class)
        form.fields['category'].widget = forms.TextInput(attrs={'placeholder':'Category','class':'border'})
        return form

    def get_context_data(self, **kwargs):
        context = super(CreateProducts, self).get_context_data(**kwargs)
        if self.request.POST:
            context['group'] = form.ProductsFormset(self.request.POST)
        else:
            context['group'] = form.ProductsFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        group = context['group']
        with transaction.atomic():
            self.object = form.save()
            if group.is_valid():
                group.instance = self.object
                group.save()
        return super(CreateProducts, self).form_valid(form)

    def get_success_url(self):
        return reverse('manage:products')

class UpdateProduct(UpdateView):
    model = Product
    template_name = 'account/update-product.html'
    form_class = form.ProductUpdate
    def get_success_url(self,*args,**kwargs):
        return reverse('manage:products')

class DeleteProduct(View):
    # @method_decorator(login_required())
    def get(self,request,*args,**kwargs):
        product_deleted = Product.objects.get(pk=self.kwargs.get('pk'))
        product_deleted.delete()
        return redirect('manage:products')

class AddProductTag(CreateView):
    model = Tag
    fields = ['tag']
    template_name = 'account/create-tag.html'

    def get_form(self, form_class = None):
        form = super(AddProductTag, self).get_form(form_class)
        form.fields['tag'].widget = forms.TextInput(attrs={'placeholder':'Tag','class':'border'})
        return form


    def get_success_url(self):
        return reverse('manage:products')

#---------------------------------------------------------------------------------
# Order's View

class all_orders(View):
    template_name = 'account/all-orders.html'
    myfilter = OrderListFilter
    # @method_decorator(login_required())
    def get(self,*args,**kwargs):
        orders = order.objects.order_by('-date_ordered')
        myfilter = self.myfilter(self.request.GET,queryset=orders)
        orders = myfilter.qs
        total_prices = []
        for o in orders:
            product_price = int(o.product.price)
            order_amount = int(o.amount)
            total = product_price * order_amount
            total_prices.append(total)
        context = {
            'myfilter' : myfilter,
            'orders':zip(orders,total_prices),
        
        }
        return render(self.request,self.template_name,context)

class Create_order(products):
    template_name = 'account/create-order.html'
    formset_class = form.OrderInlineFormset
    # @method_decorator(login_required())
    def get(self,request,*args,**kwargs):
        formset = self.formset_class()
        context = {
            'formset' : formset,
            'id' : self.kwargs.get('pk'),
        }
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        customer_access = Customer.objects.get(pk=self.kwargs.get('pk'))
        formset = self.formset_class(request.POST)
        # instance artinya mengakses field di form
        if formset.is_valid():
            for form in formset:
                form.instance.customer = customer_access
                product_amount = form.cleaned_data.get('amount')
                product_name = form.cleaned_data.get('product')
                if product_name and product_amount != 0:
                    if super().check_stock(product_name) != 0:
                        if super().check_stock(product_name) - int(product_amount) >= 0:
                            form.save()
                            super().product_reduce(product_name,product_amount)
                        else:
                            messages.warning(self.request,'Sorry, the number of products ordered exceeds the number of stock')
                            return redirect('manage:create-order',pk =self.kwargs.get('pk'))
                    else:
                        messages.warning(self.request,'Run out of stocks')
                        return redirect('manage:create-order',pk =self.kwargs.get('pk'))
                else:
                    messages.warning(self.request,'Please fill the order with valid data')
                    return redirect('manage:create-order',pk =self.kwargs.get('pk'))
        return redirect('manage:customer',pk =self.kwargs.get('pk'))

class Update_Order(products):
    form_class = form.UpdateOrderForm
    template_name = 'account/update-order.html'
    # @method_decorator(login_required())
    def get(self,request,*args,**kwargs):
        instance = order.objects.get(pk = self.kwargs.get('pk'))
        form = self.form_class(instance=instance)
        context = {
            'form':form,
            'name':instance.customer,
        }
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        instance = order.objects.get(pk = self.kwargs.get('pk'))
        form = self.form_class(self.request.POST,instance=instance)
        # When changing the order amount that is not delivered yet, the product stock need to be changed to.
        # the order previous amount need to be statisfied before form.is_valid
        # because is_valid already change the instance model into a new one with the same variable name
        previous_amount = instance.amount
        if form.is_valid():
            product_name = form.cleaned_data.get('product')
            product_amount = form.cleaned_data.get('amount')
            amount_changed = int(product_amount) - previous_amount
            if product_name and product_amount != 0:
                    if super().check_stock(product_name) != 0:
                        if super().check_stock(product_name) - int(amount_changed) >= 0:
                            form.save()
                            super().product_reduce(product_name,amount_changed)
                        else:
                            messages.warning(self.request,'Sorry, the number of products ordered exceeds the number of stock')
                            return redirect('manage:update-order',cus_pk =self.kwargs.get('cus_pk'),pk = self.kwargs.get('pk'))
                    else:
                        messages.warning(self.request,'Run out of stocks')
                        return redirect('manage:update-order',cus_pk =self.kwargs.get('cus_pk'),pk = self.kwargs.get('pk'))
            else:
                messages.warning(self.request,'Please fill the order with valid data')
                return redirect('manage:update-order',cus_pk =self.kwargs.get('cus_pk'),pk = self.kwargs.get('pk'))
        return redirect('manage:customer',pk =self.kwargs.get('cus_pk'))        


class Delete_Order(products):
    # @method_decorator(login_required())
    def get(self,request,*args,**kwargs):
        order_deleted = order.objects.get(pk=self.kwargs.get('pk'))
        if order_deleted.status == 'Pending':
            super().add_stock_back(order_deleted.product,order_deleted.amount)
        order_deleted.delete()
        return redirect('manage:customer',pk = self.kwargs.get('cus_pk'))

class Delete_Order_List(products):
    # @method_decorator(login_required()) 
    def get(self,request,*args,**kwargs):
        order_deleted = order.objects.get(pk=self.kwargs.get('pk'))
        if order_deleted.status == 'Pending':
            super().add_stock_back(order_deleted.product,order_deleted.amount)
        order_deleted.delete()
        return redirect('manage:all-orders')
