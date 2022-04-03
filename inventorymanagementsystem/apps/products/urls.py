from django.contrib import admin
from django.urls import path

from apps.products import productviews
from apps.orders import orderviews


urlpatterns = [
    path('addproducts/',productviews.add_products, name='add_products'),
    path('getproducts',productviews.get_all, name='get_all'),
    path('getproduct/<int:product_id>',productviews.get_product_by_id, name='get_product_by_id'),
    path('updateproduct/<int:product_id>',productviews.update_product, name='update_product' )
]

