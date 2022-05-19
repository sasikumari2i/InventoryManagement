from django.urls import path, include
from apps.assets import views
from rest_framework import routers
from .models import Asset, RepairingStock
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register("assets", views.AssetView, basename="asset")
router.register(
    "repairing_stocks", views.RepairingStockView, basename="repairing_stocks"
)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "asset/<str:asset_uid>/close",
        views.CloseAssetView.as_view(),
        name="close-asset",
    ),
    path(
        "repairing_stock/<str:repairing_stock_uid>/close",
        views.CloseRepairingStockView.as_view(),
        name="close-repairing-stock",
    ),
    path(
        "product/<str:product>/assets",
        views.ProductAssetView.as_view(),
        name="product-assets",
    ),
    path(
        "customer/<str:customer>/assets",
        views.CustomerAssetView.as_view(),
        name="customer-assets",
    ),
    path(
        "product/<str:product>/repairing_stocks",
        views.ProductRepairingStockView.as_view(),
        name="product_repairing_stocks",
    ),
    path(
        "asset/<str:asset>/repairing_stocks",
        views.AssetRepairingStockView.as_view(),
        name="asset_repairing_stocks",
    ),
]
