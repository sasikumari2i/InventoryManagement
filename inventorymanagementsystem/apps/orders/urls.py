from django.urls import path, include
from apps.orders import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("employees", views.EmployeeView, basename="employees")
router.register("vendors", views.VendorView, basename="vendors")
router.register("orders", views.OrderView, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
    path("delivery/<str:order_uid>/", views.DeliveryView.as_view(), name="delivery"),
    path(
        "vendor/<str:vendors>/orders",
        views.VendorOrderView.as_view(),
        name="vendor-orders",
    ),
]
