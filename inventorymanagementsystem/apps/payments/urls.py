from django.urls import path, include
from apps.payments import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('invoice', views.InvoiceView)
router.register('payment', views.PaymentView)

urlpatterns = [
    path('',include(router.urls))
]