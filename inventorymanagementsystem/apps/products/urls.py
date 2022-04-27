from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.products import views

router = routers.DefaultRouter()
router.register('products', views.ProductView)
router.register('categories', views.CategoryView)

urlpatterns = [
    path('',include(router.urls))
]

