from django.urls import path, include
from apps.orders import orderviews
from rest_framework import routers

router = routers.DefaultRouter()
router.register('customers', orderviews.CustomerView)
router.register('vendors', orderviews.VendorView)
router.register('orders', orderviews.OrderView)

urlpatterns = [
    path('',include(router.urls))
]