from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_quantity/<int:product_id>/', views.update_quantity, name='update_quantity'),
    path('delete_from_cart/<int:product_id>/', views.delete_from_cart, name='delete_from_cart'),

    path('employee_orders/', views.employee_orders, name='employee_orders'),
    path('employee_orders/sent/<int:pk>', views.orders_sent, name='order_sent'),
    path('employee_orders/completed/<int:pk>', views.orders_completed, name='order_completed'),
    path('employee_categories/', views.employee_categories, name='employee_categories'),
    path('employee_products/', views.employee_products, name='employee_products'),

    path('address/add/', views.add_address, name='add_address'),
    path('address/delete/<int:address_id>/', views.delete_address, name='delete_address'),
    path('category/add/', views.manage_category, name='add_category'),
    path('category/edit/<int:pk>/', views.manage_category, name='edit_category'),


    path('product/add/', views.manage_product, name='add_product'),
    path('product/edit/<int:pk>/', views.manage_product, name='edit_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),



]