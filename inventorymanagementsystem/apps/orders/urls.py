from django.urls import path, include
from apps.orders import views
from rest_framework import routers
from .models import Vendor
from rest_framework.urlpatterns import format_suffix_patterns


vendor_list = views.VendorView.as_view({
    'get': 'list',
    'post': 'create'
})

router = routers.DefaultRouter()
router.register('customers', views.CustomerView)
router.register('vendors', views.VendorView, basename='vendors')
router.register('orders', views.OrderView)

urlpatterns = [
    path('',include(router.urls)),
    path('delivery/<int:pk>/', views.DeliveryView.as_view(),name="delivery"),
    path('customer/<int:customer>/orders', views.CustomerOrderView.as_view(),name="customer-orders"),
    path('vendor/<int:vendor>/orders', views.VendorOrderView.as_view(), name="vendor-orders")
]
