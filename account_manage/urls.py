from django.urls import path
from . import views
app_name = 'manage'
urlpatterns = [
    #Dashboard template
    path('',views.Dashboard.as_view(),name='dashboard'),

    #product templates
    path('products/',views.products.as_view(),name='products'),
    path('products/create-products',views.CreateProducts.as_view(),name='create-category'),
    path('products/update/<int:pk>',views.UpdateProduct.as_view(),name='update-product'),
    path('products/delete/<int:pk>',views.DeleteProduct.as_view(),name='delete-product'),
    path('products/tag',views.AddProductTag.as_view(),name='add-tag'),

    #customer templates
    path('customers/',views.customers.as_view(),name='customers'),
    path('customer/<int:pk>/',views.customer.as_view(),name='customer'),
    path('create_customer/',views.Create_Customer.as_view(),name='create-customer'),
    path('update_customer/<int:pk>',views.Update_Customer.as_view(),name='update-customer'),
    path('delete_customer/<int:pk>',views.Delete_Customer.as_view(),name='delete-customer'),

    #order templates
    path('all-orders/',views.all_orders.as_view(),name='all-orders'),
    path('create_order/<int:pk>',views.Create_order.as_view(),name='create-order'),
    path('update_order/<int:cus_pk>/<int:pk>',views.Update_Order.as_view(),name='update-order'),
    path('delete_order/<int:pk>',views.Delete_Order_List.as_view(),name='delete-order-list'),
    path('delete_order/<int:cus_pk>/<int:pk>/',views.Delete_Order.as_view(),name='delete-order'),
    # path('',views.UserPage.as_view(),name='user-page'),
    # path('register/',views.UserRegistration.as_view(),name='user-register'),
    # path('login/',views.UserLogin.as_view(),name='user-login'),
    # path('logout/',views.UserLogout.as_view(),name='user-logout'),
]