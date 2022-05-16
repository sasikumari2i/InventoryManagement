from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.products import views

router = routers.DefaultRouter()
router.register('products', views.ProductView, basename='products')
router.register('categories', views.CategoryView, basename='categories')

urlpatterns = [
    path('',include(router.urls))
]

