from django.urls import path
from .views import *
urlpatterns=[
    path('accounts/login/',login_view,name='login'),
    path('accounts/signup/',signup_view,name='signup'),
    path('dashboard/',dashboard,name='dashboard'),
    path('stock_out/',stock_out,name='stock_out'),
    path('stock/',stock,name='stock'),
    path('logout',logout_view,name='logout'),
    path('report/',report_pdf,name='report'),
    path('products_in/',add_product_in_stock,name='product_in'),
    path('products_out/',sell_product,name='product_out'),
    path('add_product/',add_product,name='add_product'),
    path('delete/<int:pk>',delete_product,name='delete')
]