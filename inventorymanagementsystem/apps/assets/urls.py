from django.urls import path, include
from apps.assets import views
from rest_framework import routers
from .models import Asset, RepairingStock
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register('assets', views.AssetView, basename='asset')
router.register('repairing_stocks', views.RepairingStockView, basename='repairing_stocks')


urlpatterns = [
    path('',include(router.urls)),
]