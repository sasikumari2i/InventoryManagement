from django.urls import path, include
from apps.orders import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('customers', views.CustomerView)
router.register('vendors', views.VendorView)
router.register('orders', views.OrderView)

urlpatterns = [
    path('',include(router.urls)),
    path('delivery/<int:pk>/', views.DeliveryView.as_view(),name="delivery"),
    path('customer-orders/<int:customer>', views.CustomerOrderView.as_view(),name="customer-orders"),
    path('vendor-orders/<int:vendor>', views.VendorOrderView.as_view(), name="vendor-orders")
]
