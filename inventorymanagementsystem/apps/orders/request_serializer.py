# from rest_framework import serializers
#
# from .models import Vendor, Order,OrderProduct,Customer
# from ..products.models import Product
#
# #from ..products.serializers import ProductSerializer
#
# class RequestSerializer(serializers.Serializer):
#
#     is_sales_order = models.BooleanField(default=True, null=False)
#     order_date = models.DateField()
#     delivery_date = models.DateField()
#     vendors = models.ForeignKey(Vendor, related_name='vendor_id', on_delete=models.CASCADE, null=True)
#     customers = models.ForeignKey(Customer, related_name='customer_id', on_delete=models.CASCADE, null=False)
#     # orderproducts = [
#     #
#     # ]
#
#     {
#         "is_sales_order":false,
#         "order_date":"2022-03-02",
#         "delivery_date":"2022-03-08",
#         "vendors":2,
#         "customers":2,
#         "orderproducts" :[
#                  {"order":null,"product":14,"quantity":1},
#                  {"order":null,"product":13,"quantity":1},
#                  {"order":null,"product":12,"quantity":1}
#         ]
#     }