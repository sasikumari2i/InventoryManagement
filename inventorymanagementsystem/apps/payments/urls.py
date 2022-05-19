from django.urls import path, include
from apps.payments import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('invoice', views.InvoiceView, basename='invoice')
router.register('payment', views.PaymentView, basename='payment')

urlpatterns = [
    path('',include(router.urls)),
    path('invoice/<str:invoice_uid>/close', views.InvoiceStatusView.as_view(),name="invoice_status"),
    path('invoice/<str:invoice>/payment', views.InvoicePaymentView.as_view(), name="invoice-payment")
]