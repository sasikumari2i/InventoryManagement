from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.products import productviews
from apps.orders import orderviews

router = routers.DefaultRouter()
router.register('products', productviews.ProductView)
router.register('categories', productviews.CategoryView)

urlpatterns = [
    #path('addproducts/',productviews.add_products, name='add_products'),
    #path('getproducts',productviews.get_all, name='get_all'),
    #path('getproduct/<int:product_id>',productviews.get_product_by_id, name='get_product_by_id'),
    #path('updateproduct/<int:product_id>',productviews.update_product, name='update_product' )
    path('',include(router.urls))
]

