from django.db import models
# Create your models here.

# Customer database
class Customer(models.Model):
    username = models.CharField(max_length=150,null=True)
    email  = models.EmailField(null=True)
    telp = models.CharField(max_length = 15,null=True)
    date_created = models.DateTimeField(auto_now_add=True) #auto add now 

    def __str__(self):
        return str(self.username)

# Products database 
class Tag(models.Model):
    tag = models.CharField(max_length = 100,null=True)
    def __str__(self):
        return self.tag

class ProductGroup(models.Model):
    category = models.CharField(max_length=150,null=True)
    tag = models.ManyToManyField(Tag)
    def __str__(self):
        return self.category

class Product(models.Model):
    STATUS = (('Available','Available'),('Out of Stock','Out of Stock'))
    category = models.ForeignKey(ProductGroup,null=True,on_delete=models.CASCADE)
    product = models.CharField(max_length = 100,null=True)
    stocks = models.PositiveIntegerField(default=0,null=True)
    status = models.CharField(max_length = 100,null=True,choices=STATUS)
    price = models.FloatField(default=0,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product

# ---------------------------------------------------------------------------------

class order(models.Model):
    P_STATUS = (('Complete','Complete'),('Incomplete','Incomplete'))
    STATUS = (('Pending','Pending'),('Delivered','Delivered'))
    product = models.ForeignKey(Product,null=True,on_delete= models.CASCADE) #one product can be ordered many times
    customer = models.ForeignKey(Customer,null=True,on_delete= models.CASCADE)
    payment_status = models.CharField(max_length = 100,null=True,choices=P_STATUS)
    status = models.CharField(max_length = 100,null=True,choices=STATUS)
    amount = models.PositiveIntegerField(default=1,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Order for " + str(self.amount) + " " + str(self.product) +  " By " + str(self.customer)

