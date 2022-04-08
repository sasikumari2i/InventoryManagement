from django.urls import path, include
from apps.orders import orderviews
from rest_framework import routers

router = routers.DefaultRouter()
router.register('customers', orderviews.CustomerView)
router.register('vendors', orderviews.VendorView)
router.register('orders', orderviews.OrderView)
#router.register('orderproducts', orderviews.OrderProductView)


urlpatterns = [
    # path('getcustomers/',orderviews.get_customers, name='get_customers'),
    # path('addorders/',orderviews.add_orders, name='add_orders'),
    # path('getorders',orderviews.get_all, name='get_all'),
    # path('getorder/<int:order_id>',orderviews.get_order_by_id, name='get_order_by_id'),
    # path('updateorder/<int:order_id>',orderviews.update_order, name='update_order' )
    path('',include(router.urls))
]