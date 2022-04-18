# from .serializers import ProductSerializer
# from .models import Product
# from ..orders.models import Order
#
#
# class ProductService:
#     """Performs product related operations like add new product, get single product
#     details, get all the products, update a product details and delete product"""
#
#     def add_products(self, **product_data):
#         """To Add new products"""
#
#         product = Product.objects.create(**product_data)
#         product_serializer = ProductSerializer(product)
#         return product_serializer
#
#     def get_product_by_id(self, product_id):
#         """Get Details of the given product id"""
#
#         product_data = Product.objects.get(id=product_id)
#         product_serializer = ProductSerializer(product_data)
#         return product_serializer
#
#     def get_all(self):
#         """Get all the products available"""
#
#         products = Product.objects.all()
#         product_serializer = ProductSerializer(products, many=True)
#         return product_serializer
#
#     def update_product(self,product_id, **product_data):
#         """Update product details of the given product id"""
#
#         product_details = Product.objects.get(id=product_id)
#         for key, value in product_data.items():
#             if product_details.__getattribute__(key):
#                 product_details.__setattr__(key, value)
#             product_details.save()
#         product_serializer = ProductSerializer(product_details)
#         return product_serializer
#
#
