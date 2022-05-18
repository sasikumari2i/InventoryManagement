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
router.register('customers', views.CustomerView, basename='customers')
router.register('vendors', views.VendorView, basename='vendors')
router.register('orders', views.OrderView, basename='orders')

urlpatterns = [
    path('',include(router.urls)),
    path('delivery/<str:order_uid>/', views.DeliveryView.as_view(),name="delivery"),
    # path('customer/<int:customer>/orders', views.CustomerOrderView.as_view(),name="customer-orders"),
    path('vendor/<str:vendors>/orders', views.VendorOrderView.as_view(), name="vendor-orders")
]
