from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer
from .service import ProductService


@api_view(['POST'])
def add_products(request):
    """To Add new products"""
    product_service = ProductService()
    product_data = product_service.add_products(**request.data)
    return Response(product_data.data)


@api_view(['GET'])
def get_product_by_id(request, product_id):
    """Get Details of the given product id"""

    product_service = ProductService()
    product_data = product_service.get_product_by_id(product_id)
    return Response(product_data.data)


@api_view(['GET'])
def get_all(request):
    """Get all the products available"""

    product_service = ProductService()
    product_data = product_service.get_all()
    return Response(product_data.data)


@api_view(['PUT'])
def update_product(request, product_id):
    """Update product details of the given product id"""

    product_service = ProductService()
    product_data = product_service.update_product(product_id, **request.data)
    return Response(product_data.data)