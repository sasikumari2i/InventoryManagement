from django.urls import path
from apps.orders import orderviews


urlpatterns = [
    path('addorders/',orderviews.add_orders, name='add_orders'),
    path('getorders',orderviews.get_all, name='get_all'),
    path('getorder/<int:order_id>',orderviews.get_order_by_id, name='get_order_by_id'),
    path('updateorder/<int:order_id>',orderviews.update_order, name='update_order' )
]